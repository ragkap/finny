import json

import httpx

from app.config import settings

_request_id = 0


def _next_id() -> int:
    global _request_id
    _request_id += 1
    return _request_id


def _parse_content(result: dict | None) -> dict | None:
    """Extract the parsed JSON from MCP content response."""
    if not result:
        return None
    try:
        content = result.get("content", [])
        if content and content[0].get("type") == "text":
            return json.loads(content[0]["text"])
    except (json.JSONDecodeError, IndexError, KeyError):
        pass
    return result


class SmartKarmaMCP:
    def __init__(self):
        self.base_url = settings.smartkarma_mcp_base_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def _call(self, tool_name: str, arguments: dict) -> dict | None:
        """Make a JSON-RPC 2.0 tools/call to the MCP server."""
        try:
            resp = await self.client.post(
                self.base_url,
                json={
                    "jsonrpc": "2.0",
                    "id": _next_id(),
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments,
                    },
                },
            )
            resp.raise_for_status()
            data = resp.json()
            if "error" in data:
                return None
            return _parse_content(data.get("result"))
        except httpx.HTTPError:
            return None

    async def get_quote(self, search_string: str) -> dict | None:
        return await self._call(
            "fetch_share_price_of_company",
            {"search_string": search_string},
        )

    async def get_research(self, search_string: str) -> dict | None:
        return await self._call(
            "fetch_recent_research_by_company",
            {"search_string": search_string},
        )

    async def get_primer(self, search_string: str) -> dict | None:
        return await self._call(
            "fetch_recent_primer_by_company",
            {"search_string": search_string},
        )

    async def get_earnings(self, search_string: str) -> dict | None:
        return await self._call(
            "fetch_recent_earnings_by_company_name",
            {"search_string": search_string},
        )

    async def get_dividend(self, search_string: str) -> dict | None:
        return await self._call(
            "fetch_next_dividend_date_by_company_name",
            {"search_string": search_string},
        )

    async def get_news(self, topic: str, limit: int = 5) -> dict | None:
        return await self._call(
            "fetch_news_by_topic",
            {"topic": topic, "limit": limit},
        )

    async def get_stock_picks(self, country: str = "", sector: str = "", limit: int = 10) -> dict | None:
        params: dict = {"limit": limit}
        if country:
            params["country"] = country
        if sector:
            params["sector"] = sector
        return await self._call(
            "fetch_stock_picks_by_country_and_sector",
            params,
        )

    async def search_insights(self, query: str) -> dict | None:
        return await self._call(
            "fetch_recent_research_by_theme",
            {"search_string": query},
        )

    async def is_valid_ticker(self, search_string: str) -> bool:
        result = await self.get_quote(search_string)
        return result is not None

    async def close(self):
        await self.client.aclose()


mcp_client = SmartKarmaMCP()
