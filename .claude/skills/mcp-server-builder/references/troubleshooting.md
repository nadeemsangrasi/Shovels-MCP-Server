# MCP Server Troubleshooting

## Installation Issues

### Error: Module not found: 'mcp_use'

**Symptoms:**
```
ModuleNotFoundError: No module named 'mcp_use'
```

**Cause:** Package not installed or virtual environment not activated

**Solution (Python):**
```bash
# Install package
pip install mcp-use

# Or with uv
uv pip install mcp-use

# Verify installation
python -c "from mcp_use.server import MCPServer; print('OK')"
```

**Solution (TypeScript):**
```bash
npm install mcp-use/server
npm install zod

# Verify
node -e "console.log(require('mcp-use/server'))"
```

---

### Error: Cannot find module 'mcp-use/server'

**Symptoms:**
```
Error: Cannot find module 'mcp-use/server'
```

**Cause:** TypeScript dependencies not installed or wrong import path

**Solution:**
```bash
# Install dependencies
npm install mcp-use/server zod

# Ensure tsconfig.json is correct
# {
#   "compilerOptions": {
#     "moduleResolution": "bundler"
#   }
# }
```

---

## Server Creation Issues

### Error: Server not initializing

**Symptoms:**
Server doesn't start or crashes immediately

**Cause:** Invalid server configuration

**Solution (Python):**
```python
# Ensure all required fields are present
server = MCPServer(
    name="my-server",      # Required
    version="1.0.0",      # Required
    instructions="desc",    # Optional
    debug=True,             # Optional
)

# Check for typos in parameters
```

**Solution (TypeScript):**
```typescript
// Ensure config object is valid
const server = new MCPServer({
  name: "my-server",
  version: "1.0.0",
  description: "Optional description",
  baseUrl: process.env.MCP_URL,
  allowedOrigins: ["https://myapp.com"],
});
```

---

## Tool Registration Issues

### Error: Tool not appearing in server.tools

**Symptoms:**
Tool defined but not accessible

**Cause:** Decorator applied incorrectly or function not callable

**Solution (Python):**
```python
# Correct: Decorator before function
@server.tool()
def my_tool(input: str) -> str:
    return input

# Incorrect: Missing parentheses
@server.tool  # Wrong!
def my_tool(input: str) -> str:
    return input

# Check tool list
print([t.name for t in server.tools])
```

**Solution (TypeScript):**
```typescript
// Correct: schema defined
server.tool({
  name: "my-tool",
  schema: z.object({ input: z.string() }),
}, async ({ input }) => text(input));

// Incorrect: missing schema
server.tool({
  name: "my-tool",
  // schema missing!
}, async () => text("hello"));

// Check tools
console.log(server.tools.map(t => t.name));
```

---

### Error: Type validation failing

**Symptoms:**
Tool calls rejected with validation errors

**Cause:** Schema doesn't match actual parameters

**Solution (Python):**
```python
# Ensure type hints match actual types
@server.tool()
def process_data(
    value: int,           # Must be int
    name: str,           # Must be str
    optional: float = 1.0  # Optional with default
) -> dict:
    return {"value": value, "name": name}

# Test with correct types
process_data(42, "test")  # OK
process_data("42", "test") # Error: expected int
```

**Solution (TypeScript):**
```typescript
// Ensure zod schema matches handler params
server.tool({
  name: "process",
  schema: z.object({
    value: z.number(),      // Must be number
    name: z.string(),       // Must be string
    optional: z.number().optional(),
  }),
}, async ({ value, name }) => {
  // Types are correctly inferred
  return object({ value, name });
});
```

---

## Authentication Issues

### Error: API key not loaded

**Symptoms:**
```
Error: API_KEY is not defined
```

**Cause:** Environment variables not set or dotenv not loaded

**Solution:**
```bash
# Create .env file
echo "API_KEY=your_key_here" > .env

# Add to .gitignore
echo ".env" >> .gitignore
```

```python
# Load dotenv BEFORE using env vars
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not set in environment")
```

```typescript
// Load .env in Node
import dotenv from "dotenv";
dotenv.config();

const API_KEY = process.env.API_KEY;
if (!API_KEY) {
  throw new Error("API_KEY not set in environment");
}
```

---

### Error: Authorization header not working

**Symptoms:**
API returns 401 Unauthorized

**Cause:** Headers not formatted correctly

**Solution (Python):**
```python
import httpx

# Correct: Bearer token
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

async with httpx.AsyncClient() as client:
    response = await client.get(url, headers=headers)

# Incorrect: Missing "Bearer "
headers = {"Authorization": API_KEY}  # Wrong!
```

**Solution (TypeScript):**
```typescript
// Correct: Bearer token
const headers = {
  Authorization: `Bearer ${API_KEY}`,
  "Content-Type": "application/json",
};

const response = await fetch(url, { headers });

// Incorrect: Missing "Bearer "
const headers = { Authorization: API_KEY };  // Wrong!
```

---

## Network Issues

### Error: Connection refused

**Symptoms:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Cause:** Server not running or wrong port

**Solution:**
```python
# Check server is running
# server.py
if __name__ == "__main__":
    server.run(transport="streamable-http", host="0.0.0.0", port=8000)

# Test with curl
curl http://localhost:8000/health
```

```typescript
// Ensure server is listening
await server.listen(3000);

// Test
curl http://localhost:3000/health
```

---

### Error: Timeout

**Symptoms:**
Requests take too long and timeout

**Cause:** API slow or network issues

**Solution (Python):**
```python
import httpx

# Increase timeout
@server.tool()
async def fetch_with_timeout(url: str) -> dict:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(url)
        return response.json()
```

**Solution (TypeScript):**
```typescript
server.tool({
  name: "fetch",
  schema: z.object({ url: z.string().url() }),
}, async ({ url }) => {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 60000);

  try {
    const response = await fetch(url, { signal: controller.signal });
    clearTimeout(timeout);
    return object(await response.json());
  } finally {
    clearTimeout(timeout);
  }
});
```

---

## Docker Issues

### Error: Container exits immediately

**Symptoms:**
```
docker run ... exits with code 1
```

**Cause:** Invalid Dockerfile or entry point

**Solution:**
```dockerfile
# Check WORKDIR exists
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure entry point exists
CMD ["python", "server.py"]  # Must match filename
```

**Debug:**
```bash
# Build with no cache
docker build --no-cache -t mcp-server .

# Run interactively
docker run -it --entrypoint bash mcp-server

# Check logs
docker logs <container-id>
```

---

### Error: Port not accessible from host

**Symptoms:**
Cannot connect to server from outside container

**Cause:** EXPOSE or PORT not configured correctly

**Solution:**
```dockerfile
# Expose correct port
EXPOSE 8000

# Server binds to 0.0.0.0, not localhost
server.run(transport="streamable-http", host="0.0.0.0", port=8000)
```

```yaml
# docker-compose.yml
services:
  mcp-server:
    build: .
    ports:
      - "8000:8000"  # Map host:container
```

---

## Tool Execution Issues

### Error: Tool returns wrong type

**Symptoms:**
Tool returns value but LLM can't parse it

**Cause:** Return type doesn't match schema

**Solution (Python):**
```python
# Return matching type
@server.tool()
def get_data() -> dict:  # Returns dict
    return {"key": "value"}  # OK

@server.tool()
def get_text() -> str:  # Returns str
    return "plain text"  # OK

# Mixed types use dict
@server.tool()
def get_mixed() -> dict:
    return {
        "text": "value",
        "number": 42,
        "nested": {"key": "value"}
    }
```

**Solution (TypeScript):**
```typescript
// Use text() for strings
server.tool({
  name: "get-text",
  schema: z.object({}),
}, async () => text("plain text"));

// Use object() for objects
server.tool({
  name: "get-object",
  schema: z.object({}),
}, async () => object({ key: "value" }));

// Use mix() for both
import { mix, text, object } from "mcp-use/server";

server.tool({
  name: "get-mixed",
  schema: z.object({}),
}, async () => {
  return mix(
    text("Here's the data:"),
    object({ key: "value" })
  );
});
```

---

### Error: Tool is too slow

**Symptoms:**
Tool takes long to respond, causing timeouts

**Cause:** Expensive operations or blocking calls

**Solution (Python):**
```python
import asyncio

# Use async for I/O operations
@server.tool()
async def fetch_multiple(urls: list[str]) -> list:
    tasks = [fetch_url(url) for url in urls]
    return await asyncio.gather(*tasks)

# Add caching
from functools import lru_cache

@lru_cache(maxsize=100)
@server.tool()
def expensive_computation(key: str) -> str:
    return compute(key)
```

**Solution (TypeScript):**
```typescript
// Use Promise.all for parallel requests
server.tool({
  name: "fetch-multiple",
  schema: z.object({ urls: z.array(z.string().url()) }),
}, async ({ urls }) => {
  const results = await Promise.all(
    urls.map(url => fetch(url).then(r => r.json()))
  );
  return object({ results });
});

// Add caching
const cache = new Map<string, any>();

server.tool({
  name: "cached-computation",
  schema: z.object({ key: z.string() }),
}, async ({ key }) => {
  if (cache.has(key)) {
    return cache.get(key);
  }
  const result = await expensiveCompute(key);
  cache.set(key, result);
  return object(result);
});
```

---

## Testing Issues

### Error: Tests can't import server

**Symptoms:**
```
ImportError: cannot import name 'server' from partially initialized module
```

**Cause:** Circular imports or server initialization in module scope

**Solution (Python):**
```python
# server.py - Don't initialize server at module level
from mcp_use.server import MCPServer

def create_server():
    return MCPServer(
        name="test-server",
        version="1.0.0",
    )

server = create_server()

# tests/test_server.py
from server import create_server

def test_tool_registration():
    server = create_server()  # Fresh instance
    @server.tool()
    def test_tool() -> str:
        return "test"
    assert "test_tool" in [t.name for t in server.tools]
```

**Solution (TypeScript):**
```typescript
// server.ts - Export a factory function
export function createServer() {
  const server = new MCPServer({
    name: "test-server",
    version: "1.0.0",
  });
  return server;
}

// tests/server.test.ts
import { describe, it, expect } from "vitest";
import { createServer } from "../server";

describe("MCP Server", () => {
  it("should create server", () => {
    const server = createServer();
    expect(server).toBeDefined();
  });
});
```

---

## Debug Tips

### Enable Debug Mode

**Python:**
```python
server = MCPServer(
    name="debug-server",
    version="1.0.0",
    debug=True,
    pretty_print_jsonrpc=True,
)
```

**TypeScript:**
```typescript
const server = new MCPServer({
  name: "debug-server",
  version: "1.0.0",
  debug: true,
});
```

### Log All Calls

**Python:**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@server.tool()
def logged_tool(input: str) -> str:
    logger.debug(f"Tool called with: {input}")
    result = process(input)
    logger.debug(f"Tool returned: {result}")
    return result
```

**TypeScript:**
```typescript
console.log("Server starting...");

server.tool({
  name: "logged-tool",
  schema: z.object({ input: z.string() }),
}, async ({ input }) => {
  console.log(`Tool called with: ${input}`);
  const result = await process(input);
  console.log(`Tool returned: ${result}`);
  return object(result);
});
```

---

## Common Mistakes

### 1. Forgetting async/await

```python
# Wrong: Missing async
@server.tool()
def fetch_data(url: str) -> dict:
    response = requests.get(url)  # Blocking!
    return response.json()

# Right: Using async
@server.tool()
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### 2. Not handling errors

```python
# Wrong: No error handling
@server.tool()
def risky_operation(input: str) -> str:
    return process(input)  # Might crash!

# Right: Handle errors
@server.tool()
def safe_operation(input: str) -> str:
    try:
        return process(input)
    except Exception as e:
        return f"Error: {str(e)}"
```

### 3. Missing type hints

```python
# Wrong: No type hints
@server.tool()
def process(data):
    return str(data)

# Right: Clear type hints
@server.tool()
def process(data: str) -> str:
    return data.upper()
```

### 4. Ignoring return type

```typescript
// Wrong: Not specifying return type
server.tool({
  name: "fetch",
  schema: z.object({}),
}, async () => {
  return { data: "value" };  // Not using text() or object()!
});

// Right: Use explicit return types
import { object } from "mcp-use/server";

server.tool({
  name: "fetch",
  schema: z.object({}),
}, async () => object({ data: "value" }));
```
