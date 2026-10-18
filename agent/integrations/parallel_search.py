"""Anonymous web search through Parallel's hosted Search MCP server."""

import asyncio
import hashlib
import json
from datetime import timedelta
from typing import Any

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.config import get_config

PARALLEL_MCP_URL = "https://search.parallel.ai/mcp"
PARALLEL_USER_AGENT = "Open-SWE-Core/0.1.0"
PARALLEL_TIMEOUT_SECONDS = 30.0


async def parallel_search(query: str, num_results: int, include_contents: bool) -> str:
    arguments: dict[str, Any] = {"objective": query, "search_queries": [query]}
    try:
        thread_id = get_config().get("configurable", {}).get("thread_id")
    except RuntimeError:
        thread_id = None
    if thread_id:
        arguments["session_id"] = hashlib.sha256(str(thread_id).encode()).hexdigest()

    client = MultiServerMCPClient(
        {
            "parallel": {
                "transport": "streamable_http",
                "url": PARALLEL_MCP_URL,
                "headers": {"User-Agent": PARALLEL_USER_AGENT},
                "timeout": timedelta(seconds=PARALLEL_TIMEOUT_SECONDS),
            }
        }
    )
    async with asyncio.timeout(PARALLEL_TIMEOUT_SECONDS):
        async with client.session("parallel") as session:
            tools = await session.list_tools()
            if not any(tool.name == "web_search" for tool in tools.tools):
                raise RuntimeError("Parallel MCP does not expose web_search")
            response = await session.call_tool("web_search", arguments)

    text = "\n".join(block.text for block in response.content if block.type == "text")
    if response.isError:
        raise RuntimeError(f"Parallel search failed: {text}")
    data = response.structuredContent
    if data is None:
        data = json.loads(text)

    results = data.get("results")
    if not isinstance(results, list):
        raise ValueError("Parallel search returned no results list")
    selected = []
    for result in results[:num_results]:
        item = {key: result[key] for key in ("url", "title", "publish_date") if key in result}
        if include_contents:
            item["excerpts"] = result.get("excerpts", [])
        selected.append(item)
    return json.dumps({"results": selected, "warnings": data.get("warnings")}, ensure_ascii=False)
