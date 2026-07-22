# Shovels MCP Server — Run Guide

## Prerequisites

- **Python 3.12+** (recommended) or Python 3.9+
- **pip** (Python package manager)
- **A Shovels API key** — free at [app.shovels.ai/create-account](https://app.shovels.ai/create-account)

---

## Quick Start

### 1. Set up the environment

```bash
cd backend

# Create a virtual environment (recommended)
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure your API key

```bash
# Copy the example env file
cp .env.example .env
```

Then edit `.env` and add your key:

```env
SHOVELS_API_KEY=sk_your_key_here
```

Or set it as an environment variable (overrides `.env`):

```bash
export SHOVELS_API_KEY=sk_your_key_here
```

### 3. Start the server

```bash
# From the backend directory
uvicorn main:app --reload
```

You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## Verify It's Working

### Health Check

```bash
curl https://shovels-mcp-server.onrender.com/mcp/health
```

Expected response (healthy):

```json
{
  "status": "healthy",
  "version": "2.0.0",
  "shovels_api": "reachable"
}
```

### List MCP Tools

```bash
curl -X POST https://shovels-mcp-server.onrender.com/mcp/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}'
```

Expected: Returns `shovels_permits`, `shovels_contractors`, `shovels_decisions`, `shovels_geo`.

### Test Geo Resolution

```bash
curl -X POST https://shovels-mcp-server.onrender.com/mcp/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "shovels_geo",
      "arguments": {
        "query": "Austin, TX"
      }
    }
  }'
```

Expected: Returns geo results with a `geo_id` for Austin, TX.

---

## Using with Claude Desktop / MCP Clients

Add this to your MCP client configuration:

```json
{
  "mcpServers": {
    "shovels": {
      "url": "https://shovels-mcp-server.onrender.com/mcp/mcp",
      "headers": {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
      }
    }
  }
}
```

---

## Using with Claude Code (CLI)

```bash
# Install skillclaw if you haven't already
npx skillclaw ...

# Or configure directly
claude mcp add shovels --url https://shovels-mcp-server.onrender.com/mcp/mcp
```

---

## Deployment

### HuggingFace Spaces (Docker)

1. Push this repo to GitHub
2. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
3. Select **Docker** as the SDK
4. Connect your GitHub repo
5. Add `SHOVELS_API_KEY` to the Space secrets
6. The `Dockerfile` at `backend/Dockerfile` handles the rest

---

## Troubleshooting

| Problem                        | Likely Cause        | Fix                                    |
| ------------------------------ | ------------------- | -------------------------------------- |
| `status: "degraded"` on health | No API key set      | Add `SHOVELS_API_KEY` to `.env`        |
| `401` from Shovels API         | Invalid API key     | Check your key at app.shovels.ai       |
| `ModuleNotFoundError`          | Stale `__init__.py` | Check `src/utils/__init__.py` is empty |
| `fastmcp` install fails        | Python < 3.9        | Use Python 3.12+                       |
| Port 8000 in use               | Another service     | Use `--port 8001` flag                 |

### Port conflict

```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

### No API key for testing

If you want to test the server starts without an API key:

```bash
export SHOVELS_API_KEY=""
uvicorn main:app --reload
```

The server will start but tools will return 401 errors.

---

## Project Structure (relevant files)

```
backend/
├── main.py              # FastAPI entry point
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build
├── .env.example         # Environment template
│
├── src/
│   ├── config/
│   │   └── settings.py      # SHOVELS_API_KEY config
│   ├── models/
│   │   └── shovels_models.py # Pydantic models
│   ├── services/
│   │   └── shovels_client.py # Shovels API HTTP client
│   ├── mcp/
│   │   ├── server.py         # FastMCP initialization
│   │   └── tools.py          # 4 MCP tools
│   ├── api/
│   │   └── health.py         # /health endpoint
│   └── utils/
│       ├── logger.py         # JSON logging
│       └── retry.py          # Exponential backoff
```
