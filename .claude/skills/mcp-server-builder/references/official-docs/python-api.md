# MCP Server API Reference (Python)

## MCPServer Class

### Constructor

```python
from mcp_use.server import MCPServer

server = MCPServer(
    name: str,                      # Required - Server name
    version: str,                    # Required - Server version (semver)
    description: str = None,          # Optional - Server description
    instructions: str = None,        # Optional - Server instructions
    debug: bool = False,             # Optional - Enable debug mode
    pretty_print_jsonrpc: bool = False, # Optional - Pretty print JSON-RPC logs
    mcp_path: str = None,           # Optional - MCP API path
    inspector_path: str = None,       # Optional - Inspector path
)
```

### Methods

#### run()

Start the server with specified transport.

```python
server.run(
    transport: str,         # "stdio" or "streamable-http"
    host: str = None,      # Host to bind to (default: "localhost")
    port: int = None,      # Port to listen on
    reload: bool = False,   # Enable hot reload
)
```

**Example:**
```python
# stdio transport (default)
server.run(transport="stdio")

# HTTP transport with hot reload
server.run(
    transport="streamable-http",
    host="0.0.0.0",
    port=8000,
    reload=True,
)
```

#### tool()

Decorator to register a function as a tool.

```python
@server.tool(name: str | None = None)
def tool_function(*args, **kwargs) -> Any:
    """Tool description."""
    return result
```

**Example:**
```python
@server.tool()
def calculate(expression: str) -> float:
    """Evaluate a mathematical expression."""
    return eval(expression)

@server.tool(name="custom-name")
def my_function(input: str) -> str:
    """Custom tool with name override."""
    return f"Processed: {input}"
```

#### resource()

Decorator to register a function as a resource.

```python
@server.resource(uri: str | None = None)
def resource_function() -> Any:
    """Resource description."""
    return data
```

**Example:**
```python
@server.resource()
def config() -> dict:
    """Server configuration."""
    return {"version": "1.0.0", "env": "prod"}

@server.resource(uri="config://settings")
def settings() -> dict:
    """Settings resource with custom URI."""
    return {"theme": "dark"}
```

### Properties

- `tools`: List of registered tools
- `resources`: List of registered resources

---

## Tool Decorator

### Type Hints

Tools should use Python type hints for automatic schema generation.

```python
@server.tool()
def typed_tool(
    string_param: str,
    int_param: int,
    float_param: float,
    bool_param: bool,
    optional_param: str = "default",
) -> dict:
    """Tool with typed parameters."""
    return {
        "string": string_param,
        "int": int_param,
        "float": float_param,
        "bool": bool_param,
        "optional": optional_param,
    }
```

### Async Tools

Tools can be async functions.

```python
import httpx

@server.tool()
async def fetch_url(url: str) -> dict:
    """Async tool for HTTP requests."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### Docstrings

Docstrings provide tool descriptions to LLMs.

```python
@server.tool()
def search_web(query: str, limit: int = 10) -> list:
    """
    Search the web for results.

    Args:
        query: Search query string
        limit: Maximum number of results (1-100)

    Returns:
        List of search results with title and URL
    """
    return [
        {"title": "Result 1", "url": "https://example.com/1"},
        {"title": "Result 2", "url": "https://example.com/2"},
    ]
```

---

## MCPRouter Class

Organize tools into groups/routers.

```python
from mcp_use.server import MCPRouter

router = MCPRouter()

@router.tool()
def tool1(arg: str) -> str:
    return arg

@router.tool()
def tool2(arg: int) -> int:
    return arg * 2

# Mount router to server
server.mount_router("/api", router)
```

---

## Transport Options

### stdio

Standard input/output for local connections.

```python
server.run(transport="stdio")
```

### streamable-http

HTTP transport with SSE support.

```python
server.run(
    transport="streamable-http",
    host="0.0.0.0",
    port=8000,
)
```

### Transport Comparison

| Transport | Use Case | Pros | Cons |
|-----------|-----------|------|------|
| stdio | Local CLI, direct connection | Simple, no networking | Remote access requires proxy |
| streamable-http | Web, remote access | Browser-friendly, CORS support | Requires HTTP setup |

---

## Configuration

### Environment Variables

```bash
# API keys
API_KEY=your_api_key_here
DATABASE_URL=postgresql://...

# Server configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

```python
import os
from dotenv import load_dotenv

load_dotenv()

server = MCPServer(
    name="my-server",
    version="1.0.0",
    debug=os.getenv("DEBUG", "false").lower() == "true",
)
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@server.tool()
def logged_tool(input: str) -> str:
    logger.info(f"Tool called with: {input}")
    return input
```

---

## Migration from FastMCP

The mcp-use library provides compatibility with FastMCP.

```python
# Old FastMCP
from fastmcp import FastMCP

server = FastMCP(name="my-server")

# New mcp-use - Compatibility mode
from mcp_use.server import FastMCP

server = FastMCP(name="my-server")

# Recommended - Full features
from mcp_use.server import MCPServer

server = MCPServer(name="my-server", debug=True)
```

---

## Best Practices

### 1. Type Safety

Always use type hints for parameters and return values.

```python
@server.tool()
def process(data: dict[str, any]) -> str:
    return json.dumps(data)
```

### 2. Error Handling

Handle errors gracefully and return user-friendly messages.

```python
@server.tool()
def safe_operation(input: str) -> str:
    try:
        return process(input)
    except ValueError as e:
        return f"Validation error: {e}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### 3. Async for I/O

Use async functions for network or database operations.

```python
@server.tool()
async def fetch_data(id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/api/data/{id}")
        return response.json()
```

### 4. Documentation

Provide clear docstrings for LLM understanding.

```python
@server.tool()
def calculate_tax(amount: float, rate: float = 0.08) -> float:
    """
    Calculate tax for a given amount.

    Args:
        amount: Base amount before tax
        rate: Tax rate as decimal (default: 0.08 for 8%)

    Returns:
        Tax amount calculated as amount * rate
    """
    return amount * rate
```

### 5. Caching

Use caching for expensive operations.

```python
from functools import lru_cache

@lru_cache(maxsize=100)
@server.tool()
def expensive_lookup(key: str) -> str:
    """Cached lookup operation."""
    # Expensive computation
    return result
```
