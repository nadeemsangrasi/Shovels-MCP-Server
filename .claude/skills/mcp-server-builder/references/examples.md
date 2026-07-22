# MCP Server Examples

## Example 1: Weather API Server (Python)

Complete production-ready MCP server exposing weather data.

### Project Structure
```
weather-mcp/
├── server.py
├── requirements.txt
├── .env
└── Dockerfile
```

### Implementation

**requirements.txt:**
```txt
mcp-use>=1.0.0
httpx>=0.25.0
python-dotenv>=1.0.0
```

**.env:**
```bash
WEATHER_API_KEY=your_key_here
WEATHER_API_BASE_URL=https://api.weather.com/v1
```

**server.py:**
```python
from mcp_use.server import MCPServer
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

server = MCPServer(
    name="weather-server",
    version="1.0.0",
    instructions="Weather data API server",
)

@server.tool()
async def get_current_weather(city: str) -> dict:
    """Get current weather for a city.

    Args:
        city: Name of the city
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{os.getenv('WEATHER_API_BASE_URL')}/current",
            params={"city": city, "key": os.getenv('WEATHER_API_KEY')},
        )
        response.raise_for_status()
        return response.json()

@server.tool()
async def get_forecast(city: str, days: int = 5) -> dict:
    """Get weather forecast.

    Args:
        city: Name of the city
        days: Number of days to forecast (1-10)
    """
    if days < 1 or days > 10:
        raise ValueError("days must be between 1 and 10")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{os.getenv('WEATHER_API_BASE_URL')}/forecast",
            params={"city": city, "days": days, "key": os.getenv('WEATHER_API_KEY')},
        )
        response.raise_for_status()
        return response.json()

@server.resource()
def server_info() -> dict:
    """Server configuration and status."""
    return {
        "name": "weather-server",
        "version": "1.0.0",
        "endpoints": ["current", "forecast"],
    }

if __name__ == "__main__":
    server.run(transport="stdio")
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

RUN groupadd -r weather && useradd -r -g weather weather
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R weather:weather /app
USER weather

CMD ["python", "server.py"]
```

### Testing

**tests/test_weather.py:**
```python
import pytest
from httpx import AsyncClient, Response
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_get_current_weather():
    from server import server

    mock_response = AsyncMock(spec=Response)
    mock_response.json.return_value = {"city": "London", "temp": 20, "condition": "sunny"}
    mock_response.raise_for_status = lambda: None

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        result = await get_current_weather("London")
        assert result["city"] == "London"

def test_forecast_validation():
    with pytest.raises(ValueError):
        get_forecast("London", days=15)
```

---

## Example 2: GitHub Integration Server (TypeScript)

MCP server for interacting with GitHub API.

### Project Structure
```
github-mcp/
├── src/
│   ├── server.ts
│   └── index.ts
├── package.json
├── tsconfig.json
└── .env
```

### Implementation

**package.json:**
```json
{
  "name": "github-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "mcp-use/server": "^1.0.0",
    "zod": "^3.22.0",
    "octokit": "^3.0.0",
    "dotenv": "^16.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "tsx": "^4.0.0",
    "@types/node": "^20.0.0"
  }
}
```

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

**src/server.ts:**
```typescript
import { MCPServer, text, object } from "mcp-use/server";
import { z } from "zod";
import { Octokit } from "octokit";

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN,
});

const server = new MCPServer({
  name: "github-server",
  version: "1.0.0",
  description: "GitHub API integration",
});

server.tool({
  name: "get-repo",
  description: "Get repository information",
  schema: z.object({
    owner: z.string().describe("Repository owner"),
    repo: z.string().describe("Repository name"),
  }),
}, async ({ owner, repo }) => {
  const { data } = await octokit.rest.repos.get({
    owner,
    repo,
  });

  return object({
    name: data.name,
    description: data.description,
    stars: data.stargazers_count,
    language: data.language,
    url: data.html_url,
  });
});

server.tool({
  name: "list-issues",
  description: "List repository issues",
  schema: z.object({
    owner: z.string().describe("Repository owner"),
    repo: z.string().describe("Repository name"),
    state: z.enum(["open", "closed", "all"]).default("open"),
    limit: z.number().min(1).max(100).default(20),
  }),
}, async ({ owner, repo, state, limit }) => {
  const { data } = await octokit.rest.issues.listForRepo({
    owner,
    repo,
    state,
    per_page: limit,
  });

  return text(
    `Found ${data.length} ${state} issues:\n` +
    data.map((issue: any) =>
      `#${issue.number}: ${issue.title} (${issue.html_url})`
    ).join("\n")
  );
});

server.tool({
  name: "create-issue",
  description: "Create a new issue",
  schema: z.object({
    owner: z.string().describe("Repository owner"),
    repo: z.string().describe("Repository name"),
    title: z.string().describe("Issue title"),
    body: z.string().optional().describe("Issue description"),
  }),
}, async ({ owner, repo, title, body }) => {
  const { data } = await octokit.rest.issues.create({
    owner,
    repo,
    title,
    body,
  });

  return object({
    number: data.number,
    url: data.html_url,
    title: data.title,
  });
});

server.resource({
  name: "user-info",
  uri: "github://user",
  description: "Current authenticated user info",
}, async () => {
  const { data } = await octokit.rest.users.getAuthenticated();
  return object({
    login: data.login,
    name: data.name,
    email: data.email,
  });
});

export { server };
```

**src/index.ts:**
```typescript
import { server } from "./server.js";

await server.listen(3000);
console.log("GitHub MCP server running on port 3000");
```

---

## Example 3: Rate-Limited API Server (Python)

Server with built-in rate limiting and caching.

```python
from mcp_use.server import MCPServer
from functools import lru_cache
import asyncio
from datetime import datetime, timedelta
import json

server = MCPServer(
    name="rate-limited-server",
    version="1.0.0",
)

# Rate limiter state
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

rate_limiter = RateLimiter(calls=5, period=60)

@server.tool()
async def rate_limited_fetch(query: str) -> dict:
    """Fetch data with rate limiting (5 calls/minute)."""
    await rate_limiter.acquire()

    # Simulate API call
    await asyncio.sleep(0.1)
    return {"query": query, "result": "data", "timestamp": datetime.now().isoformat()}

@lru_cache(maxsize=100)
@server.tool()
def cached_lookup(key: str) -> str:
    """Cached lookup operation."""
    # Expensive operation
    import time
    time.sleep(0.5)
    return f"Result for {key}"

if __name__ == "__main__":
    server.run(transport="stdio")
```

---

## Example 4: Multi-Tool Server with Error Handling

Comprehensive server with multiple tools and robust error handling.

```python
from mcp_use.server import MCPServer
import httpx
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = MCPServer(
    name="multi-tool-server",
    version="1.0.0",
    instructions="Server with multiple API integrations",
)

API_BASE_URL = "https://api.example.com"
API_TIMEOUT = 30.0

async def api_call(
    endpoint: str,
    params: Optional[dict] = None,
    timeout: float = API_TIMEOUT
) -> dict:
    """Make API call with error handling."""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(
                f"{API_BASE_URL}/{endpoint}",
                params=params,
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        raise ValueError(f"API error: {e.response.status_code}")
    except httpx.TimeoutException:
        logger.error("API timeout")
        raise ValueError("Request timed out")
    except Exception as e:
        logger.error(f"API error: {e}")
        raise ValueError(f"API request failed: {str(e)}")

@server.tool()
async def search_documents(query: str, limit: int = 10) -> dict:
    """Search documents.

    Args:
        query: Search query
        limit: Maximum results (1-100)
    """
    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")

    return await api_call("search", params={"q": query, "limit": limit})

@server.tool()
async def get_document(id: str) -> dict:
    """Get document by ID.

    Args:
        id: Document ID
    """
    if not id or len(id) < 3:
        raise ValueError("Invalid document ID")

    return await api_call(f"documents/{id}")

@server.tool()
async def analyze_text(text: str, model: str = "default") -> dict:
    """Analyze text with ML model.

    Args:
        text: Text to analyze
        model: Model to use (default, advanced)
    """
    if not text or len(text.strip()) == 0:
        raise ValueError("Text cannot be empty")

    if model not in ["default", "advanced"]:
        raise ValueError("Invalid model name")

    return await api_call("analyze", params={"text": text, "model": model})

@server.resource()
def server_status() -> dict:
    """Server health status."""
    return {
        "status": "healthy",
        "tools": ["search_documents", "get_document", "analyze_text"],
        "version": "1.0.0",
    }

if __name__ == "__main__":
    server.run(transport="stdio", debug=True)
```

---

## Example 5: OAuth2 Authenticated Server (TypeScript)

Server with OAuth2 token management.

```typescript
import { MCPServer, object } from "mcp-use/server";
import { z } from "zod";

interface OAuthToken {
  access_token: string;
  refresh_token: string;
  expires_at: number;
}

class OAuth2Client {
  private token: OAuthToken | null = null;

  async refreshAccessToken(): Promise<string> {
    // Refresh token logic
    const response = await fetch(process.env.OAUTH_TOKEN_URL!, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        grant_type: "refresh_token",
        refresh_token: process.env.OAUTH_REFRESH_TOKEN!,
        client_id: process.env.OAUTH_CLIENT_ID!,
        client_secret: process.env.OAUTH_CLIENT_SECRET!,
      }),
    });

    const data = await response.json();
    this.token = {
      access_token: data.access_token,
      refresh_token: data.refresh_token,
      expires_at: Date.now() + data.expires_in * 1000,
    };
    return this.token.access_token;
  }

  async getAccessToken(): Promise<string> {
    if (!this.token || Date.now() >= this.token.expires_at - 60000) {
      return await this.refreshAccessToken();
    }
    return this.token.access_token;
  }
}

const oauth = new OAuth2Client();

const server = new MCPServer({
  name: "oauth-server",
  version: "1.0.0",
  description: "OAuth2 authenticated API server",
});

server.tool({
  name: "fetch-data",
  description: "Fetch data from OAuth2 protected API",
  schema: z.object({
    resource: z.string().describe("Resource path"),
  }),
}, async ({ resource }) => {
  const token = await oauth.getAccessToken();

  const response = await fetch(
    `https://api.example.com/${resource}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    }
  );

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return object(await response.json());
});

await server.listen(3000);
```
