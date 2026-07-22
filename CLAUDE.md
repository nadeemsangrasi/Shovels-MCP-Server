# Shovels MCP Server

An MCP server wrapping the Shovels public REST API (`api.shovels.ai/v2`). Search U.S. building permits, contractors, and zoning/land-use decisions through 4 consolidated MCP tools.

## Architecture

**Stack:** FastAPI + FastMCP (Python) deployed on HuggingFace Spaces (Docker).

**No database, no vector store, no frontend.** The server is a thin HTTP proxy to the Shovels API with retry logic and credit-header surfacing.

## File Structure

```
backend/
├── main.py                           # FastAPI entry point
├── Dockerfile                        # HuggingFace Spaces deployment
├── requirements.txt                  # Python dependencies
├── pyproject.toml                    # Pytest configuration
│
├── src/
│   ├── config/
│   │   └── settings.py               # Pydantic Settings (SHOVELS_API_KEY)
│   │
│   ├── models/
│   │   └── shovels_models.py         # Pydantic models for all API shapes
│   │
│   ├── services/
│   │   └── shovels_client.py         # Async HTTP client for api.shovels.ai/v2
│   │
│   ├── mcp/
│   │   ├── server.py                 # FastMCP initialization
│   │   └── tools.py                  # 4 MCP tools (permits, contractors, decisions, geo)
│   │
│   ├── api/
│   │   └── health.py                 # GET /health
│   │
│   └── utils/
│       ├── logger.py                 # Structured JSON logging
│       └── retry.py                  # Exponential backoff for API calls
```

## MCP Tools

### `shovels_permits`
Search U.S. building permits by `geo_id` + date range, or fetch full records by ID.

- **Search mode** (no `id`): compact rows with `resource` URI
- **Fetch mode** (`id` supplied): full permit record (property data, fees, tags)

### `shovels_contractors`
Search contractors active in a geography, or fetch full profiles by ID.

- Same dual-mode pattern as permits

### `shovels_decisions`
Search zoning/land-use decisions (rezonings, variances), or fetch full records by ID.

- Same dual-mode pattern
- **ZIP codes not supported** — state/place geo_ids only

### `shovels_geo`
Resolve free-text addresses/places to `geo_id`. Tries address → city → county → jurisdiction → state.

**Required first step** before any search tool — those endpoints reject free-text addresses.

## API Endpoints

```
GET  /health         # Service status (public, no auth)
POST /mcp            # MCP Streamable HTTP endpoint
  └── tools/shovels_permits       # Search or fetch permits
  └── tools/shovels_contractors   # Search or fetch contractors
  └── tools/shovels_decisions     # Search or fetch decisions
  └── tools/shovels_geo           # Resolve geo_id
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SHOVELS_API_KEY` | Yes | — | Shovels API key (get one at app.shovels.ai) |
| `SHOVELS_API_BASE` | No | `https://api.shovels.ai/v2` | API base URL override |

## Development

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Start dev server
SHOVELS_API_KEY=sk_... uvicorn main:app --reload

# Health check
curl http://localhost:8000/health
```

## Known Constraints

- Free trial: **250 requests flat** (any size)
- `geo_id` + date range required for all searches
- `contractor_name` requires **3+ characters**
- `decision_q` capped at **100 characters**
- All monetary values in **cents**
