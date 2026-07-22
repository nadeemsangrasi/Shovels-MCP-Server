# MCP Server Quick Reference

## Python (FastMCP)

### Server Creation

**Basic server:**
```python
from mcp_use.server import MCPServer

server = MCPServer(
    name="my-server",
    version="1.0.0",
    instructions="Server description",
)
```

**With debug mode:**
```python
server = MCPServer(
    name="my-server",
    version="1.0.0",
    debug=True,
    pretty_print_jsonrpc=True,
)
```

### Tool Definition

**Simple tool:**
```python
@server.tool()
def my_tool(input: str) -> str:
    """Tool description."""
    return f"Processed: {input}"
```

**Async tool:**
```python
@server.tool()
async def async_tool(query: str) -> dict:
    """Async tool description."""
    # async operation
    return {"result": query}
```

**With custom name:**
```python
@server.tool(name="custom_name")
def my_function() -> str:
    return "hello"
```

### Resource Definition

**Simple resource:**
```python
@server.resource()
def config() -> dict:
    """Server configuration."""
    return {"version": "1.0.0"}
```

**With URI:**
```python
@server.resource(uri="config://settings")
def settings() -> dict:
    return {"theme": "dark"}
```

### Running Server

**stdio transport:**
```python
server.run(transport="stdio")
```

**HTTP transport:**
```python
server.run(
    transport="streamable-http",
    host="0.0.0.0",
    port=8000,
)
```

**With hot reload:**
```python
server.run(
    transport="streamable-http",
    reload=True,
)
```

### Authentication

**API key from env:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

@server.tool()
def authenticated_call() -> dict:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    # API call
    return {}
```

### HTTP Client

**Basic HTTP request:**
```python
import httpx

@server.tool()
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

**With timeout and retries:**
```python
@server.tool()
async def fetch_with_retry(url: str) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        for attempt in range(3):
            try:
                response = await client.get(url)
                return response.json()
            except httpx.HTTPError:
                continue
        raise ValueError("Request failed after 3 attempts")
```

### Error Handling

**Try-except:**
```python
@server.tool()
def safe_operation(input: str) -> str:
    try:
        result = risky_operation(input)
        return f"Success: {result}"
    except ValueError as e:
        return f"Validation error: {e}"
    except Exception as e:
        return f"Error: {str(e)}"
```

**Raise custom error:**
```python
@server.tool()
def validate_input(value: int) -> str:
    if value < 0 or value > 100:
        raise ValueError("Value must be between 0 and 100")
    return f"Valid: {value}"
```

### Rate Limiting

**Simple rate limiter:**
```python
import asyncio
from datetime import datetime, timedelta

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

limiter = RateLimiter(calls=5, period=60)

@server.tool()
async def rate_limited(query: str) -> dict:
    await limiter.acquire()
    # API call
    return {}
```

### Caching

**LRU cache:**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
@server.tool()
def cached_lookup(key: str) -> str:
    # Expensive operation
    return f"Result for {key}"
```

**Custom cache:**
```python
cache = {}

@server.tool()
def cached_get(key: str) -> str:
    if key in cache:
        return cache[key]
    result = expensive_operation(key)
    cache[key] = result
    return result
```

---

## TypeScript (MCP SDK)

### Server Creation

**Basic server:**
```typescript
import { MCPServer } from "mcp-use/server";

const server = new MCPServer({
  name: "my-server",
  version: "1.0.0",
  description: "Server description",
});
```

**With base URL:**
```typescript
const server = new MCPServer({
  name: "my-server",
  version: "1.0.0",
  baseUrl: process.env.MCP_URL || "http://localhost:3000",
});
```

**With allowed origins:**
```typescript
const server = new MCPServer({
  name: "my-server",
  version: "1.0.0",
  allowedOrigins: ["https://myapp.com"],
});
```

### Tool Definition

**Simple tool:**
```typescript
import { text } from "mcp-use/server";

server.tool({
  name: "greet",
  description: "Greet someone",
  schema: z.object({
    name: z.string().describe("Person's name"),
  }),
}, async ({ name }) =>
  text(`Hello, ${name}!`)
);
```

**Object return:**
```typescript
import { object } from "mcp-use/server";

server.tool({
  name: "get-info",
  schema: z.object({ id: z.string() }),
}, async ({ id }) =>
  object({ id, name: "Item", value: 42 })
);
```

**Mixed return:**
```typescript
import { mix, text, object } from "mcp-use/server";

server.tool({
  name: "fetch-data",
  schema: z.object({ query: z.string() }),
}, async ({ query }) => {
  const data = { query, result: "found" };
  return mix(text(`Found: ${query}`), object(data));
});
```

### Resource Definition

**Simple resource:**
```typescript
server.resource({
  name: "config",
  uri: "config://settings",
  description: "Server configuration",
}, async () =>
  object({ version: "1.0.0", env: "prod" })
);
```

### Running Server

**Listen on port:**
```typescript
await server.listen(3000);
console.log("Server running on port 3000");
```

**Default port:**
```typescript
await server.listen();
```

### Authentication

**API key from env:**
```typescript
const API_KEY = process.env.API_KEY!;

server.tool({
  name: "fetch-data",
  schema: z.object({ endpoint: z.string() }),
}, async ({ endpoint }) => {
  const response = await fetch(
    `https://api.example.com/${endpoint}`,
    { headers: { Authorization: `Bearer ${API_KEY}` } }
  );
  return object(await response.json());
});
```

### HTTP Client

**Basic fetch:**
```typescript
server.tool({
  name: "fetch-url",
  schema: z.object({ url: z.string().url() }),
}, async ({ url }) => {
  const response = await fetch(url);
  return object(await response.json());
});
```

**With timeout:**
```typescript
server.tool({
  name: "fetch-with-timeout",
  schema: z.object({ url: z.string().url() }),
}, async ({ url }) => {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 30000);

  try {
    const response = await fetch(url, { signal: controller.signal });
    clearTimeout(timeout);
    return object(await response.json());
  } catch (error) {
    clearTimeout(timeout);
    throw new Error("Request timed out");
  }
});
```

### Error Handling

**Try-catch:**
```typescript
server.tool({
  name: "safe-operation",
  schema: z.object({ input: z.string() }),
}, async ({ input }) => {
  try {
    const result = await riskyOperation(input);
    return object({ success: true, result });
  } catch (error) {
    return object({ success: false, error: String(error) });
  }
});
```

**Throw error:**
```typescript
server.tool({
  name: "validate",
  schema: z.object({ value: z.number() }),
}, async ({ value }) => {
  if (value < 0 || value > 100) {
    throw new Error("Value must be between 0 and 100");
  }
  return object({ valid: true, value });
});
```

### Rate Limiting

**Simple rate limiter:**
```typescript
class RateLimiter {
  private requests: number[] = [];

  constructor(private calls: number, private period: number) {}

  async acquire(): Promise<void> {
    const now = Date.now();
    this.requests = this.requests.filter(t => t > now - this.period * 1000);

    if (this.requests.length >= this.calls) {
      const wait = this.requests[0] + this.period * 1000 - now;
      await new Promise(r => setTimeout(r, Math.max(0, wait)));
    }

    this.requests.push(Date.now());
  }
}

const limiter = new RateLimiter(5, 60);

server.tool({
  name: "rate-limited",
  schema: z.object({ query: z.string() }),
}, async ({ query }) => {
  await limiter.acquire();
  // API call
  return object({});
});
```

---

## Zod Schemas (TypeScript)

### Basic Types

**String:**
```typescript
z.string().describe("A string value")
```

**Number:**
```typescript
z.number().describe("A numeric value")
```

**Boolean:**
```typescript
z.boolean().describe("A boolean flag")
```

### Validation

**Optional:**
```typescript
z.string().optional()
```

**Default:**
```typescript
z.string().default("default-value")
```

**Enum:**
```typescript
z.enum(["option1", "option2", "option3"])
```

**Range:**
```typescript
z.number().min(0).max(100)
```

**Email:**
```typescript
z.string().email()
```

**URL:**
```typescript
z.string().url()
```

### Objects

**Nested object:**
```typescript
z.object({
  name: z.string(),
  age: z.number(),
  email: z.string().email().optional(),
})
```

**With transform:**
```typescript
z.string().transform(val => val.toLowerCase())
```

---

## Docker Config

**Python Dockerfile:**
```dockerfile
FROM python:3.11-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R appuser:appuser /app
USER appuser

CMD ["python", "server.py"]
```

**docker-compose.yml:**
```yaml
version: "3.8"

services:
  mcp-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_KEY=${API_KEY}
    restart: unless-stopped
```

---

## Testing Patterns

**Python pytest:**
```python
import pytest

def test_tool_exists():
    from server import server
    assert "my_tool" in [t.name for t in server.tools]

@pytest.mark.asyncio
async def test_async_tool():
    from server import async_tool
    result = await async_tool("test")
    assert result["result"] == "test"
```

**TypeScript vitest:**
```typescript
import { describe, it, expect } from "vitest";

describe("MCP Server", () => {
  it("should register tool", () => {
    expect(server.tools.length).toBeGreaterThan(0);
  });

  it("should have tool with correct name", () => {
    const tool = server.tools.find(t => t.name === "fetch-data");
    expect(tool).toBeDefined();
  });
});
```
