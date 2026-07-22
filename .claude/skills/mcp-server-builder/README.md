# MCP Server Builder Skill

Build production-ready MCP (Model Context Protocol) servers that expose APIs and external services as tools for LLMs.

## What is MCP?

The Model Context Protocol (MCP) enables LLMs to safely interact with external services by defining tools that the model can call. An MCP server is an application that exposes tools, resources, and prompts that LLMs can use.

**Use this skill to:**
- Build MCP servers in Python (FastMCP) or TypeScript (MCP SDK)
- Design tools that wrap external APIs
- Handle authentication and rate limiting
- Deploy servers with Docker
- Test and evaluate MCP implementations

**NOT for:** consuming existing MCP servers (use them directly)

## Quick Start

### Python (FastMCP)

```bash
pip install mcp-use
```

```python
from mcp_use.server import MCPServer

server = MCPServer(
    name="my-server",
    version="1.0.0",
)

@server.tool()
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    server.run(transport="stdio")
```

### TypeScript (MCP SDK)

```bash
npm install mcp-use/server zod
```

```typescript
import { MCPServer, text } from "mcp-use/server";
import { z } from "zod";

const server = new MCPServer({
  name: "my-server",
  version: "1.0.0",
});

server.tool({
  name: "greet",
  description: "Greet someone",
  schema: z.object({
    name: z.string().describe("Person's name"),
  }),
}, async ({ name }) =>
  text(`Hello, ${name}!`)
);

await server.listen(3000);
```

## Installation

Copy the skill directory to `.claude/skills/`:

```bash
cp -r mcp-server-builder ~/.claude/skills/
# or
cp -r mcp-server-builder /path/to/project/.claude/skills/
```

Restart Claude Code:

```bash
claude reload
```

## Usage Examples

### Example 1: Weather API Server

```bash
# Ask Claude Code:
"Build an MCP server that integrates with OpenWeatherMap API"
```

The skill guides you through:
1. Defining weather tools (current weather, forecast)
2. Adding API authentication
3. Handling errors and rate limiting
4. Testing the server

**See:** `references/examples.md#example-1-weather-api-server`

### Example 2: GitHub Integration

```bash
# Ask Claude Code:
"Create an MCP server for GitHub API with tools to fetch repos and create issues"
```

The skill covers:
1. Octokit client setup
2. Tool definitions (get-repo, list-issues, create-issue)
3. Resource definitions (user-info)
4. Testing with mocked responses

**See:** `references/examples.md#example-2-github-integration`

### Example 3: Docker Deployment

```bash
# Ask Claude Code:
"Deploy my MCP server to Docker"
```

The skill provides:
1. Production-ready Dockerfile
2. Environment variable setup
3. Multi-stage builds
4. Security best practices

**See:** `references/examples.md#docker`

## Features

### Python Support
- **FastMCP compatible** - Drop-in replacement for existing FastMCP code
- **Async/await** - Full async support for concurrent operations
- **Type hints** - Automatic schema generation from type annotations
- **Error handling** - Built-in error recovery patterns
- **Decorators** - Clean `@server.tool()` and `@server.resource()` syntax

### TypeScript Support
- **Zod schemas** - Type-safe parameter validation
- **Response mixins** - `text()`, `object()`, `mix()` for flexible returns
- **Chainable API** - Fluent method chaining for server setup
- **HTTP proxy** - Access to Hono/Express HTTP methods
- **Environment config** - Built-in support for `baseUrl` and `allowedOrigins`

### Both Languages
- **stdio & HTTP transports** - Choose based on deployment needs
- **Authentication** - Environment variables, API keys, OAuth2 patterns
- **Rate limiting** - Built-in patterns for API quotas
- **Caching** - LRU cache for expensive operations
- **Docker ready** - Containerization examples included
- **Testing** - pytest (Python) and vitest (TypeScript) patterns
- **Logging** - Structured logging with debug modes

## Documentation

### Core Files

- **SKILL.md** - Main workflow (8 phases, < 500 lines)
- **README.md** - This file

### Reference Documentation

- **examples.md** - 5 complete, production-ready examples
- **quick-reference.md** - Code snippets and patterns
- **troubleshooting.md** - Common errors and solutions
- **official-docs/**
  - `python-api.md` - Python MCPServer API reference
  - `typescript-api.md` - TypeScript MCPServer API reference

## Workflow Overview

The skill follows an 8-phase workflow:

1. **Project Setup** - Install dependencies (FastMCP or MCP SDK)
2. **Create Server Instance** - Initialize MCPServer with configuration
3. **Define Tools** - Create functions that wrap external APIs
4. **Add Authentication** - Configure API keys and credentials
5. **Add Resources** (Optional) - Expose static data as resources
6. **Run Server** - Choose transport (stdio or HTTP)
7. **Docker Deployment** - Containerize for production
8. **Create Evaluation Tests** - Test tools with pytest/vitest

## Decision Trees

### Language Choice
- Python team? → Use FastMCP (simpler decorators)
- TypeScript team? → Use MCP SDK (type-safe schemas)
- Familiar with async? → Either works
- Need performance? → TypeScript slightly faster
- Rapid prototyping? → Python easier

### Transport Choice
- Local development? → Use `stdio` (default)
- Remote access? → Use `streamable-http`
- Docker deployment? → Use HTTP with `host: 0.0.0.0`
- LLM integration? → Depends on LLM client setup

### Authentication Method
- Simple API key? → Environment variable + Bearer header
- OAuth2 required? → Implement token refresh logic
- Custom auth? → Add to tool implementation
- No auth? → Document as public endpoint

## Common Patterns

### API Integration with Error Handling

```python
@server.tool()
async def fetch_data(endpoint: str) -> dict:
    """Fetch from external API."""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{API_BASE_URL}/{endpoint}",
                headers={"Authorization": f"Bearer {API_KEY}"},
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        return {"error": f"API error: {e}"}
```

### Rate Limiting

```python
class RateLimiter:
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.requests = []

    async def acquire(self):
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.period)
        self.requests = [r for r in self.requests if r > cutoff]
        if len(self.requests) >= self.calls:
            wait = (self.requests[0] + timedelta(seconds=self.period) - now).total_seconds()
            await asyncio.sleep(max(0, wait))
        self.requests.append(now)
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
@server.tool()
def expensive_lookup(key: str) -> str:
    return compute(key)
```

## Testing

### Python with pytest

```python
def test_tool_exists():
    from server import server
    assert "my_tool" in [t.name for t in server.tools]

@pytest.mark.asyncio
async def test_async_tool():
    from server import async_tool
    result = await async_tool("test")
    assert result["result"] == "test"
```

**Run tests:**
```bash
pytest tests/ -v
```

### TypeScript with vitest

```typescript
import { describe, it, expect } from "vitest";

describe("MCP Server", () => {
  it("should register tools", () => {
    expect(server.tools.length).toBeGreaterThan(0);
  });
});
```

**Run tests:**
```bash
npm test
```

## Docker Deployment

### Build

```bash
docker build -t mcp-server .
```

### Run Locally

```bash
docker run -p 8000:8000 \
  -e API_KEY=your_key_here \
  mcp-server
```

### docker-compose

```yaml
version: "3.8"

services:
  mcp-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_KEY=${API_KEY}
      - DATABASE_URL=${DATABASE_URL}
    restart: unless-stopped
```

## Troubleshooting

### Problem: Tool not appearing
**Solution:** Check decorator syntax and function signature

### Problem: API key not loading
**Solution:** Ensure `.env` file exists and `load_dotenv()` is called

### Problem: Connection refused
**Solution:** Check server is running and using correct host/port

### Problem: Timeout errors
**Solution:** Increase timeout, add retry logic, check API performance

**See:** `references/troubleshooting.md` for complete troubleshooting guide

## Best Practices

1. **Type safety** - Always use type hints (Python) or Zod schemas (TypeScript)
2. **Error handling** - Wrap API calls in try-catch
3. **Async operations** - Use async for I/O operations
4. **Documentation** - Add clear docstrings/descriptions
5. **Caching** - Cache expensive operations
6. **Rate limiting** - Respect API quotas
7. **Environment variables** - Never hardcode secrets
8. **Testing** - Test tools independently before integration

## Supported MCP SDK Versions

- **Python:** `mcp-use >= 1.0.0`
- **TypeScript:** `mcp-use/server >= 1.0.0`, `zod >= 3.20.0`

## Resources

- **MCP Specification:** https://modelcontextprotocol.io
- **mcp-use Documentation:** https://mcp-use.com
- **Official Examples:** `references/examples.md`
- **Quick Reference:** `references/quick-reference.md`
- **API Documentation:**
  - Python: `references/official-docs/python-api.md`
  - TypeScript: `references/official-docs/typescript-api.md`

## Tips

- Start with **stdio transport** for rapid development
- Use **HTTP transport** when you need remote access
- Prefer **async functions** for I/O operations
- Test tools **independently** before integration
- Document tool **purpose and parameters** clearly
- Use **environment variables** for all secrets
- Consider **rate limiting** early in development
- Deploy with **Docker** for consistency

## Contact & Support

For issues or questions:
1. Check `references/troubleshooting.md`
2. Review example implementations in `references/examples.md`
3. Consult official docs in `references/official-docs/`
4. Use Context7 MCP: `/fetching-library-docs mcp-use`

## Version History

**v1.0.0 (2026-01-11)**
- Initial release
- Python FastMCP support
- TypeScript MCP SDK support
- 5 complete examples
- Docker deployment guide
- Comprehensive troubleshooting

## License

This skill follows the same license as Claude Code and the projects it integrates with.
