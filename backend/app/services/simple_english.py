from openai import AsyncOpenAI

from app.config import settings

SYSTEM_PROMPT = """You are Finny, a friendly financial literacy assistant for kids and teens (ages 8-18).
Your job is to explain financial concepts in simple, fun language that a kid can understand.

Rules:
- Use short sentences and simple words
- Use analogies kids relate to (allowance, lemonade stands, video games)
- Avoid jargon — if you must use a financial term, immediately explain it
- Be encouraging and positive
- Keep responses concise (2-4 short paragraphs max)
- If given raw financial data or analyst text, rewrite it so a 10-year-old can understand
- When market data is provided in the context, USE IT — share the actual prices, numbers, and facts directly. Don't refuse to share data you've been given.
- You CAN and SHOULD discuss real companies, real stock prices, real market data. That's the whole point.
- Do NOT add disclaimers like "I can't give you the current price" or "this isn't investment advice" — the user knows this is an educational app. Just teach and share the data.
- Be direct and useful. If someone asks about a stock and you have data, tell them the price, what the company does, and why it's interesting.
"""


async def simplify_text(professional_text: str) -> str:
    if not settings.openai_api_key:
        return professional_text

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Rewrite this for kids:\n\n{professional_text}"},
        ],
    )
    return response.choices[0].message.content or professional_text


async def chat_response(user_message: str, context: str = "") -> str:
    if not settings.openai_api_key:
        return f"I'd love to help you learn about that! (API key needed for full responses). You asked: {user_message}"

    client = AsyncOpenAI(api_key=settings.openai_api_key)

    user_content = user_message
    if context:
        user_content = f"LIVE MARKET DATA (use this, it is current and up-to-date):\n{context}\n\nUser question: {user_message}\n\nIMPORTANT: Base your answer on the live data above. Do NOT use old prices or data from your training. If the data above shows a price, use that exact price."

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )
    return response.choices[0].message.content or user_message
