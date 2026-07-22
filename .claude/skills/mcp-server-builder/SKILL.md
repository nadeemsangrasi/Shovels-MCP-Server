---
name: mcp-server-builder
description: Guides creation of high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK). Covers tool design, authentication, Docker deployment, and evaluation creation. NOT when consuming existing MCP servers (use the server directly).
version: 1.0.0
allowed-tools: Bash, Read, Write, Edit, mcp__context7__query-docs, mcp__context7__resolve-library-id
author: Claude Code
tags: [mcp, server, python, typescript, tools, api]
---

# MCP Server Builder

## Overview

Build production-ready MCP (Model Context Protocol) servers that expose external APIs and services as tools for LLMs. Supports Python (FastMCP) and TypeScript/Node (MCP SDK) with authentication, Docker deployment, and evaluation testing.

**See:** `references/official-docs/` for complete MCP documentation

## When to Use

**Activate when:**
- "create MCP server", "build MCP server", "MCP server setup"
- "expose API as MCP tool", "MCP integration"
- "FastMCP server", "MCP SDK TypeScript"
- "MCP authentication", "MCP Docker deployment"
- "MCP evaluation", "test MCP server"

**NOT for:** consuming existing MCP servers (use server directly)

## Prerequisites

**Required:**
- Python 3.8+ or Node.js 18+
- `mcp-use` package (Python) or `mcp-use/server` (TypeScript)

**Optional:**
- External API credentials
- Docker (for deployment)
- Testing frameworks (pytest, vitest)

**See:** `references/examples.md#setup` for installation guides

## Instructions

### Phase 1: Project Setup

**Python (FastMCP):**
```bash
pip install mcp-use
# or with uv
uv pip install mcp-use
```

**TypeScript (MCP SDK):**
```bash
npm install mcp-use/server zod
npm install -D typescript @types/node
```

**Validation:**
- `python -c "from mcp_use.server import MCPServer; print('OK')"`
- `npx tsc --version` (TypeScript installed)

**See:** `references/examples.md#setup-complete`

### Phase 2: Create Server Instance

**Python - Basic Server:**
```python
from mcp_use.server import MCPServer

server = MCPServer(
    name="my-server",
    version="1.0.0",
    instructions="Server for external API",
    debug=True,
)
```

**TypeScript - Basic Server:**
```typescript
import { MCPServer } from "mcp-use/server";

const server = new MCPServer({
  name: "my-server",
  version: "1.0.0",
  description: "MCP server for external API",
});
```

**Validation:**
- Server instantiates without errors
- Name/version are set correctly

**See:** `references/examples.md#server-instance`

### Phase 3: Define Tools

**Python - Tool Decorator:**
```python
@server.tool()
def fetch_data(query: str) -> str:
    """Fetch data from external API."""
    # API call logic
    return f"Result for {query}"
```

**TypeScript - Tool Definition:**
```typescript
import { z } from "zod";

server.tool({
  name: "fetch-data",
  description: "Fetch data from external API",
  schema: z.object({
    query: z.string().describe("Search query"),
  }),
}, async ({ query }) => {
  // API call logic
  return { result: query };
});
```

**Key principles:**
- Clear function names
- Type-safe parameters (zod for TS)
- Descriptive docstrings
- Handle errors gracefully

**Validation:**
- Tool appears in server.tools list
- Schema validation works
- Returns correct type

**See:** `references/examples.md#tool-definition`

### Phase 4: Add Authentication

**Python - API Key from env:**
```python
from dotenv import load_dotenv
import os

load_dotenv()

@server.tool()
def authenticated_call(endpoint: str) -> str:
    headers = {"Authorization": f"Bearer {os.getenv('API_KEY')}"}
    # API call with headers
    return "data"
```

**TypeScript - API Key from env:**
```typescript
const API_KEY = process.env.API_KEY!;

server.tool({
  name: "authenticated-call",
  schema: z.object({ endpoint: z.string() }),
}, async ({ endpoint }) => {
  const headers = { Authorization: `Bearer ${API_KEY}` };
  // API call with headers
  return { data: "..." };
});
```

**Validation:**
- Environment variables loaded
- Headers set correctly
- Authenticated calls succeed

**See:** `references/examples.md#authentication`

### Phase 5: Add Resources (Optional)

**Python - Static Resource:**
```python
@server.resource()
def config() -> dict:
    """Server configuration."""
    return { "version": "1.0.0", "env": "prod" }
```

**TypeScript - Static Resource:**
```typescript
server.resource({
  name: "config",
  uri: "config://settings",
  description: "Server configuration",
}, async () => ({
  version: "1.0.0",
  env: "prod",
}));
```

**See:** `references/examples.md#resources`

### Phase 6: Run Server

**Python - stdio transport:**
```python
if __name__ == "__main__":
    server.run(transport="stdio")
```

**Python - HTTP transport (development):**
```python
server.run(
    transport="streamable-http",
    host="0.0.0.0",
    port=8000,
    reload=True,
)
```

**TypeScript - Listen:**
```typescript
await server.listen(3000);
console.log("Server running");
```

**Validation:**
- Server starts without errors
- Tools accessible via transport
- Connection works

**See:** `references/examples.md#run-server`

### Phase 7: Docker Deployment

**Dockerfile (Python):**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "server.py"]
```

**Validation:**
- `docker build -t mcp-server .`
- `docker run -p 8000:8000 mcp-server`

**See:** `references/examples.md#docker`

### Phase 8: Create Evaluation Tests

**Python - pytest:**
```python
from mcp_use.server import MCPServer

def test_tool_exists():
    server = MCPServer(name="test", version="1.0.0")
    @server.tool()
    def sample(x: str) -> str:
        return x
    assert "sample" in [t.name for t in server.tools]
```

**TypeScript - vitest:**
```typescript
import { describe, it, expect } from "vitest";

describe("MCP Server", () => {
  it("should register tool", () => {
    const server = new MCPServer({ name: "test", version: "1.0.0" });
    server.tool({ name: "sample", schema: z.object({}) }, async () => ({}));
    expect(server.tools).toHaveLength(1);
  });
});
```

**Validation:**
- All tests pass
- Coverage > 80%

**See:** `references/examples.md#evaluation`

## Common Patterns

### Pattern 1: HTTP API Integration
```python
import httpx

@server.tool()
async def fetch_user(user_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/api/users/{user_id}")
        return response.json()
```

**See:** `references/examples.md#http-integration`

### Pattern 2: Rate Limiting
```python
from asyncio import sleep

@server.tool()
async def rate_limited_call(query: str) -> str:
    await sleep(1)  # Rate limit
    return f"Result: {query}"
```

**See:** `references/examples.md#rate-limiting`

### Pattern 3: Error Handling
```python
@server.tool()
def safe_operation(input: str) -> str:
    try:
        # Operation
        return "success"
    except Exception as e:
        return f"Error: {str(e)}"
```

**See:** `references/examples.md#error-handling`

### Pattern 4: Pagination
```python
@server.tool()
def fetch_items(page: int = 1) -> list:
    items = api_call(page)
    return items
```

**See:** `references/examples.md#pagination`

### Pattern 5: Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
@server.tool()
def cached_lookup(key: str) -> str:
    return expensive_operation(key)
```

**See:** `references/examples.md#caching`

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Module not found` | Package not installed | Install `mcp-use` or `mcp-use/server` |
| `Tool not registered` | Decorator syntax error | Check function signature |
| `Invalid schema` | Wrong zod definition | Verify schema types match |
| `Connection refused` | Port in use or wrong | Check host/port configuration |
| `Auth failed` | Missing/wrong API key | Verify environment variables |
| `Timeout` | API slow | Add timeout/retry logic |
| `CORS error` | Origins not allowed | Set `allowedOrigins` in config |

**See:** `references/troubleshooting.md` for detailed solutions

## Decision Trees

### Which Language?
```
Python preferred? → Yes → Use FastMCP (simpler decorators)
                → No → Use TypeScript (MCP SDK)

Need async? → Yes → Both support async
            → No → Python sync is simpler

Team familiarity? → Python → Use Python
                → JS/TS → Use TypeScript
```

### Which Transport?
```
Local testing? → Use stdio (default)
Remote access? → Use streamable-http/SSE
Docker? → Use HTTP with host: 0.0.0.0
Production? → Use stdio with orchestration
```

### Authentication Method?
```
Simple API key? → Use env var + Authorization header
OAuth? → Add token refresh logic
Custom auth? → Implement in tool logic
No auth? → Document as public endpoint
```

## RunConfig Options

**Python:**
```python
server.run(
    transport="streamable-http",
    host="0.0.0.0",
    port=8000,
    reload=True,
    debug=True,
)
```

**TypeScript:**
```typescript
const server = new MCPServer({
  name: "my-server",
  version: "1.0.0",
  baseUrl: process.env.MCP_URL,
  allowedOrigins: ["https://myapp.com"],
});
```

**See:** `references/quick-reference.md#config`

## References

**Local Documentation:**
- Complete examples: `references/examples.md`
- Code snippets: `references/quick-reference.md`
- Troubleshooting: `references/troubleshooting.md`
- Official docs: `references/official-docs/`

**External:**
- MCP Use (Python): https://mcp-use.com/docs/python
- MCP Use (TypeScript): https://mcp-use.com/docs/typescript
- MCP Spec: https://modelcontextprotocol.io

**Use Context7 MCP:** `/fetching-library-docs` for latest docs

## Tips for Success

1. Start with stdio transport for local testing
2. Use environment variables for all secrets
3. Add type hints (Python) or zod schemas (TS)
4. Test tools independently before integration
5. Document tool purpose in docstrings
6. Handle errors with user-friendly messages
7. Consider rate limiting for external APIs
8. Use Docker for consistent deployments

**See:** `references/examples.md#best-practices`
