from fastapi import APIRouter, HTTPException

from app.services.smartkarma_mcp import mcp_client

router = APIRouter(prefix="/api/market", tags=["market"])


@router.get("/quote/{ticker}")
async def get_quote(ticker: str):
    quote = await mcp_client.get_quote(ticker)
    if not quote:
        raise HTTPException(status_code=404, detail=f"No data found for '{ticker}'")
    return quote


@router.get("/research/{ticker}")
async def get_research(ticker: str):
    research = await mcp_client.get_research(ticker)
    if not research:
        raise HTTPException(status_code=404, detail=f"No research found for '{ticker}'")
    return research


@router.get("/earnings/{ticker}")
async def get_earnings(ticker: str):
    earnings = await mcp_client.get_earnings(ticker)
    if not earnings:
        raise HTTPException(status_code=404, detail=f"No earnings found for '{ticker}'")
    return earnings


@router.get("/dividend/{ticker}")
async def get_dividend(ticker: str):
    dividend = await mcp_client.get_dividend(ticker)
    if not dividend:
        raise HTTPException(status_code=404, detail=f"No dividend info for '{ticker}'")
    return dividend


@router.get("/news/{topic}")
async def get_news(topic: str, limit: int = 5):
    news = await mcp_client.get_news(topic, limit=limit)
    if not news:
        raise HTTPException(status_code=404, detail=f"No news found for '{topic}'")
    return news
