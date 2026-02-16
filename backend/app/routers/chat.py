import json
import re

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.firebase_auth import get_firebase_user
from app.models.user import User
from app.services import scoring
from app.services.simple_english import chat_response
from app.services.smartkarma_mcp import mcp_client

router = APIRouter(prefix="/api/chat", tags=["chat"])

TICKER_PATTERN = re.compile(r"\b([A-Z]{1,5})\b")
JARGON_PATTERN = re.compile(
    r"what (?:is|are) (?:a |an |the )?(dividend|stock|bond|etf|index|market cap|p/e ratio|portfolio|inflation|interest rate|mutual fund|ipo|bull market|bear market)",
    re.IGNORECASE,
)


class ChatRequest(BaseModel):
    message: str


class QuoteData(BaseModel):
    company: str = ""
    exchange: str = ""
    currency: str = "USD"
    price: str = "0"
    day_change_percent: str = "0"
    market_cap_usd: float | None = None
    pe: float | None = None
    dividend_yield: float | None = None
    pb: float | None = None
    url: str | None = None


class InsightCardData(BaseModel):
    title: str
    text: str
    chart_data: list[dict] | None = None
    ticker: str | None = None
    quote: QuoteData | None = None


class ChatResponse(BaseModel):
    reply: str
    insight_cards: list[InsightCardData] = []
    xp_earned: int = 0
    new_badges: list[dict] = []
    finny_score: int = 0
    level: int = 1


def _summarize_result(data: dict | None) -> str:
    """Convert MCP result dict to a text summary for the LLM context."""
    if not data:
        return ""
    try:
        return json.dumps(data, default=str, ensure_ascii=False)[:2000]
    except Exception:
        return str(data)[:2000]


def _build_quote_data(quote: dict) -> QuoteData:
    """Extract structured quote data from MCP response."""
    company = quote.get("company", "").strip()
    price_data = quote.get("price_data", {})
    stats = quote.get("current_stats", {})

    return QuoteData(
        company=company,
        exchange=price_data.get("exchange", ""),
        currency=price_data.get("currency", "USD"),
        price=price_data.get("price", "0"),
        day_change_percent=price_data.get("dayChangePercentage", "0"),
        market_cap_usd=stats.get("market_value_usd"),
        pe=stats.get("pe"),
        dividend_yield=stats.get("div_yld"),
        pb=stats.get("pb"),
        url=quote.get("url"),
    )


@router.post("", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    firebase_user: dict = Depends(get_firebase_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.firebase_uid == firebase_user["uid"]).first()
    if not user:
        user = User(
            firebase_uid=firebase_user["uid"],
            display_name=firebase_user.get("name", "Finny Learner"),
            avatar_url=firebase_user.get("picture"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    xp_earned = 0
    insight_cards: list[InsightCardData] = []
    context_parts: list[str] = []

    # Check streak
    streak_result = scoring.check_streak(db, user.id)
    if streak_result["bonus_awarded"]:
        xp_earned += 100

    # Award first message badge
    scoring.award_points(db, user.id, "first_message")

    msg_lower = req.message.lower()

    # Detect tickers
    tickers_found = TICKER_PATTERN.findall(req.message)
    valid_tickers = []
    for t in tickers_found[:3]:
        if await mcp_client.is_valid_ticker(t):
            valid_tickers.append(t)

    # Fetch MCP data for each valid ticker
    for ticker in valid_tickers:
        quote = await mcp_client.get_quote(ticker)
        research = await mcp_client.get_research(ticker)

        if quote:
            context_parts.append(f"Share price data for {ticker}: {_summarize_result(quote)}")
            qd = _build_quote_data(quote)
            insight_cards.append(InsightCardData(
                title=qd.company or ticker,
                text="",
                ticker=ticker,
                quote=qd,
            ))

        if research:
            context_parts.append(f"Analyst research for {ticker}: {_summarize_result(research)}")

        # Dividend-specific lookup
        if "dividend" in msg_lower:
            dividend = await mcp_client.get_dividend(ticker)
            if dividend:
                context_parts.append(f"Dividend info for {ticker}: {_summarize_result(dividend)}")

        # Earnings-specific lookup
        if any(w in msg_lower for w in ("earning", "revenue", "profit", "eps")):
            earnings = await mcp_client.get_earnings(ticker)
            if earnings:
                context_parts.append(f"Earnings for {ticker}: {_summarize_result(earnings)}")

        metadata = {"ticker": ticker}
        if "dividend" in msg_lower:
            metadata["topic"] = "dividend"

        points = scoring.award_points(db, user.id, "ticker_identify", metadata)
        xp_earned += points

    # If no tickers found but message mentions a company name, try fuzzy search
    if not valid_tickers:
        # Try treating the whole message as a company search
        company_words = re.findall(r"(?:about|price of|tell me about|how is)\s+(.+?)[\?\.]?$", msg_lower)
        if company_words:
            search = company_words[0].strip()
            quote = await mcp_client.get_quote(search)
            if quote:
                context_parts.append(f"Share price data: {_summarize_result(quote)}")
                qd = _build_quote_data(quote)
                insight_cards.append(InsightCardData(
                    title=qd.company or search.title(),
                    text="",
                    quote=qd,
                ))
                points = scoring.award_points(db, user.id, "ticker_identify", {"search": search})
                xp_earned += points

    # Detect jargon questions
    jargon_match = JARGON_PATTERN.search(req.message)
    if jargon_match:
        term = jargon_match.group(1)
        theme_research = await mcp_client.search_insights(term)
        if theme_research:
            context_parts.append(f"Research on '{term}': {_summarize_result(theme_research)}")

        news = await mcp_client.get_news(term, limit=3)
        if news:
            context_parts.append(f"Recent news on '{term}': {_summarize_result(news)}")

        points = scoring.award_points(db, user.id, "jargon_quest", {"term": term})
        xp_earned += points

    # If no context was gathered from tickers or jargon, always fetch
    # live market data so the LLM never falls back to stale training data
    if not context_parts:
        news = await mcp_client.get_news("stocks", limit=5)
        if news:
            context_parts.append(f"Today's market news: {_summarize_result(news)}")

        # For stock recommendation questions, fetch top picks
        if any(w in msg_lower for w in ("best stock", "recommend", "should i buy", "top stock", "which stock", "good stock", "pick")):
            picks = await mcp_client.get_stock_picks(country="", sector="", limit=5)
            if picks:
                context_parts.append(f"Top-rated stocks by SmartScore: {_summarize_result(picks)}")

        # For broad theme questions, search insights
        theme_research = await mcp_client.search_insights(req.message)
        if theme_research:
            context_parts.append(f"Related research: {_summarize_result(theme_research)}")

    # Generate response
    context = "\n".join(context_parts) if context_parts else ""
    reply = await chat_response(req.message, context)

    # Check badge eligibility
    new_badges = scoring.check_badge_eligibility(db, user.id)

    db.refresh(user)

    return ChatResponse(
        reply=reply,
        insight_cards=insight_cards,
        xp_earned=xp_earned,
        new_badges=new_badges,
        finny_score=user.finny_score,
        level=user.level,
    )
