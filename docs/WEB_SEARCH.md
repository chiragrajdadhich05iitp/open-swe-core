# Web search

The coding, chat, and review agents use [Parallel Search MCP](https://docs.parallel.ai/integrations/mcp/search-mcp)
for web search when `EXA_API_KEY` is unset. Search uses Fast mode and needs no account or API key.
Queries are sent to `https://search.parallel.ai/mcp`. Parallel returns source URLs and relevant
excerpts rather than full page contents; `include_contents=false` omits those excerpts, and
`num_results` limits the returned results. The existing `fetch_url` tool can read individual pages.
The anonymous service has usage limits; failures are returned to the agent as search errors.

An existing `EXA_API_KEY` keeps Exa as the selected provider. Set
`OPEN_SWE_WEB_SEARCH_PROVIDER=parallel` or `exa` to choose explicitly, or `disabled` to prevent
web searches. Selecting Exa requires `EXA_API_KEY`. Unknown settings return a configuration
error. A failed search does not switch providers. Parallel requests time out after 30 seconds
and use the existing sandbox-result files or bounded inline results when no sandbox is available.

For example, configure the server environment to disable web search:

```bash
OPEN_SWE_WEB_SEARCH_PROVIDER=disabled
```

Leave `OPEN_SWE_WEB_SEARCH_PROVIDER` unset or empty for automatic selection. To use Parallel
while retaining an Exa key for other applications, set `OPEN_SWE_WEB_SEARCH_PROVIDER=parallel`.

The agents keep the existing `web_search(query, num_results=5, include_contents=True)` tool.
No additional tool permissions or provider credentials are granted by this integration.
