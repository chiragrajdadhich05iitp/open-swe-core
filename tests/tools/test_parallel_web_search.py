import asyncio
import hashlib
import importlib
import json
import sys
from typing import Any
from unittest.mock import AsyncMock

import httpx
import pytest
from langchain.agents import create_agent
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_mcp_adapters import sessions

from agent.integrations import parallel_search
from agent.tools import web_search

search_module = importlib.import_module("agent.tools.web_search")


@pytest.fixture(autouse=True)
def isolated_search_environment(monkeypatch):
    for name in ("EXA_API_KEY", "PARALLEL_API_KEY", "OPEN_SWE_WEB_SEARCH_PROVIDER"):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def mcp_server(monkeypatch):
    requests: list[tuple[httpx.Request, dict[str, Any]]] = []
    state: dict[str, Any] = {
        "result": {
            "results": [
                {"url": "https://docs.python.org/3/", "title": "Python", "excerpts": ["docs"]},
                {"url": "https://example.com/", "title": "Example", "excerpts": ["extra"]},
            ]
        }
    }

    async def handle(request):
        body = json.loads(request.content)
        requests.append((request, body))
        method = body["method"]
        if method == "notifications/initialized":
            return httpx.Response(202)
        if method == "initialize":
            result = {
                "protocolVersion": "2025-03-26",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "fixture", "version": "1"},
            }
        elif method == "tools/list":
            result = {"tools": [{"name": "web_search", "inputSchema": {"type": "object"}}]}
        elif method == "tools/call":
            state["started"].set()
            if state.get("hang"):
                try:
                    await asyncio.Event().wait()
                finally:
                    state["cancelled"].set()
            if state.get("http_error"):
                return httpx.Response(state["http_error"])
            if state.get("malformed"):
                return httpx.Response(200, text="not JSON")
            result = {
                "content": [{"type": "text", "text": json.dumps(state["result"])}],
                "isError": state.get("is_error", False),
            }
            if not state.get("text_only"):
                result["structuredContent"] = state["result"]
        else:
            raise AssertionError(method)
        return httpx.Response(200, json={"jsonrpc": "2.0", "id": body["id"], "result": result})

    state["started"] = asyncio.Event()
    state["cancelled"] = asyncio.Event()

    def factory(**kwargs):
        return httpx.AsyncClient(transport=httpx.MockTransport(handle), **kwargs)

    monkeypatch.setattr(sessions, "create_mcp_http_client", factory)
    return requests, state


class ScriptedSearchModel(FakeMessagesListChatModel):
    def bind_tools(self, tools, **kwargs):
        return self

    async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs):
        if isinstance(messages[-1], ToolMessage):
            content = messages[-1].content
            assert isinstance(content, str)
            output = json.loads(content)
            assert output["success"] is True
            source = json.loads(output["results"])["results"][0]
            answer = AIMessage(content=f"Documentation: {source['url']} ({source['title']})")
        else:
            answer = AIMessage(
                content="",
                tool_calls=[
                    {"id": "search-1", "name": "web_search", "args": {"query": "python docs"}}
                ],
            )
        return ChatResult(generations=[ChatGeneration(message=answer)])


async def test_registered_tool_agent_dispatch_consumes_anonymous_results(mcp_server):
    requests, _ = mcp_server
    model = ScriptedSearchModel(responses=[])
    agent = create_agent(model=model, tools=[web_search])
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Find Python docs"}]},
        {"configurable": {"thread_id": "conversation-1"}},
    )
    assert result["messages"][-1].content == "Documentation: https://docs.python.org/3/ (Python)"
    methods = [body["method"] for _, body in requests]
    assert methods == ["initialize", "notifications/initialized", "tools/list", "tools/call"]
    for request, _ in requests:
        assert str(request.url) == "https://search.parallel.ai/mcp"
        assert request.headers["user-agent"] == "Open-SWE-Core/0.1.0"
        assert "authorization" not in request.headers
    assert requests[-1][1]["params"] == {
        "name": "web_search",
        "arguments": {
            "objective": "python docs",
            "search_queries": ["python docs"],
            "session_id": hashlib.sha256(b"conversation-1").hexdigest(),
        },
    }


@pytest.mark.parametrize("text_only", [True, False])
async def test_result_limits_and_content_choice(mcp_server, text_only):
    _, state = mcp_server
    state["text_only"] = text_only
    result = await web_search("python docs", num_results=1, include_contents=False)
    assert result["success"] is True
    assert json.loads(result["results"])["results"] == [
        {"url": "https://docs.python.org/3/", "title": "Python"}
    ]


async def test_parallel_results_use_existing_sandbox_jsonl(monkeypatch, mcp_server):
    writes = []

    async def write(name, content, extension):
        writes.append((name, content, extension))
        return "/workspace/search.jsonl"

    monkeypatch.setattr(search_module, "write_sandbox_output", write)
    result = await web_search("python docs")
    assert result["results_path"] == "/workspace/search.jsonl"
    assert result["results"] is None
    assert writes[0][0::2] == ("web-search", "jsonl")
    decoded = "".join(json.loads(line)["text"] for line in writes[0][1].splitlines())
    assert json.loads(decoded)["results"][0]["excerpts"] == ["docs"]
    assert result["result_chars"] == len(decoded)


@pytest.mark.parametrize("override", [None, "exa"])
@pytest.mark.parametrize("include_contents", [True, False])
async def test_configured_exa_is_preserved(monkeypatch, mcp_server, override, include_contents):
    requests, _ = mcp_server
    calls = []

    class Exa:
        def __init__(self, api_key):
            assert api_key == "saved-key"

        def search(self, *args, **kwargs):
            calls.append(("search", args, kwargs))
            return "Exa results"

        def search_and_contents(self, *args, **kwargs):
            calls.append(("contents", args, kwargs))
            return "Exa results"

    monkeypatch.setenv("EXA_API_KEY", "saved-key")
    if override:
        monkeypatch.setenv("OPEN_SWE_WEB_SEARCH_PROVIDER", override)
    monkeypatch.setitem(sys.modules, "exa_py", type("ExaModule", (), {"Exa": Exa}))
    result = await web_search("python docs", 2, include_contents)
    assert result["results"] == "Exa results"
    assert calls == [
        (
            "contents" if include_contents else "search",
            ("python docs",),
            {"num_results": 2, "type": "auto", **({"text": True} if include_contents else {})},
        )
    ]
    assert requests == []


async def test_explicit_parallel_overrides_exa_without_sending_credentials(monkeypatch, mcp_server):
    requests, _ = mcp_server
    monkeypatch.setenv("EXA_API_KEY", "saved-key")
    monkeypatch.setenv("PARALLEL_API_KEY", "ambient-key")
    monkeypatch.setenv("OPEN_SWE_WEB_SEARCH_PROVIDER", "parallel")
    assert (await web_search("python docs"))["success"] is True
    assert all("authorization" not in request.headers for request, _ in requests)


@pytest.mark.parametrize("provider", ["disabled", "unknown", "exa"])
async def test_disabled_or_invalid_configuration_never_connects(monkeypatch, mcp_server, provider):
    requests, _ = mcp_server
    monkeypatch.setenv("OPEN_SWE_WEB_SEARCH_PROVIDER", provider)
    result = await web_search("python docs")
    assert result["success"] is False
    assert result["error"]
    assert requests == []


@pytest.mark.parametrize("query,count", [("", 5), ("   ", 5), ("docs", 0)])
async def test_invalid_arguments_never_connect(mcp_server, query, count):
    requests, _ = mcp_server
    assert (await web_search(query, count))["success"] is False
    assert requests == []


@pytest.mark.parametrize("failure", ["is_error", "malformed", "http_error", "missing_results"])
async def test_mcp_errors_return_failure(monkeypatch, mcp_server, failure):
    _, state = mcp_server
    monkeypatch.setattr(parallel_search, "PARALLEL_TIMEOUT_SECONDS", 0.2)
    if failure == "missing_results":
        state["result"] = {"unexpected": []}
    else:
        state[failure] = 503 if failure == "http_error" else True
    result = await web_search("python docs")
    assert result["success"] is False
    assert result["results"] is None
    assert result["error"]


async def test_exa_failure_does_not_fall_back(monkeypatch, mcp_server):
    requests, _ = mcp_server
    monkeypatch.setenv("EXA_API_KEY", "saved-key")
    exa = AsyncMock(side_effect=RuntimeError("Exa unavailable"))
    monkeypatch.setattr(search_module.asyncio, "to_thread", exa)
    result = await web_search("python docs")
    assert result["success"] is False
    assert "Exa unavailable" in result["error"]
    assert requests == []


async def test_timeout_cancels_inflight_http(monkeypatch, mcp_server):
    _, state = mcp_server
    state["hang"] = True
    monkeypatch.setattr(parallel_search, "PARALLEL_TIMEOUT_SECONDS", 0.1)
    result = await web_search("python docs")
    assert result["success"] is False
    assert "TimeoutError" in result["error"]
    assert state["cancelled"].is_set()


async def test_cancellation_propagates_and_closes_transport(mcp_server):
    _, state = mcp_server
    state["hang"] = True
    task = asyncio.create_task(web_search("python docs"))
    await asyncio.wait_for(state["started"].wait(), timeout=2)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert state["cancelled"].is_set()


async def test_tool_omission_preserves_agent_permissions(mcp_server):
    requests, _ = mcp_server
    model = FakeMessagesListChatModel(responses=[AIMessage(content="No search allowed")])
    agent = create_agent(model=model, tools=[])
    await agent.ainvoke({"messages": [{"role": "user", "content": "Find docs"}]})
    assert requests == []
