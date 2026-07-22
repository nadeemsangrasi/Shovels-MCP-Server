# Shovels MCP Server

An MCP server wrapping the Shovels public REST API (`api.shovels.ai/v2`). Search U.S. building permits, contractors, and geo-resolve locations through 4 consolidated MCP tools — a 1:1 mirror of the Shovels CLI's business logic, delivered over MCP instead of a shell.

## Architecture

**Stack:** FastAPI + FastMCP (Python) deployed on HuggingFace Spaces (Docker).

**No database, no vector store, no frontend.** The server is a thin HTTP proxy to the Shovels API with retry logic and credit-header surfacing.

## File Structure

```
backend/
├── main.py                           # FastAPI entry point + API key middleware
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
│   │   └── tools.py                  # 4 MCP tools + progressive-disclosure helpers
│   │
│   ├── api/
│   │   └── health.py                 # GET /health
│   │
│   └── utils/
│       ├── logger.py                 # Structured JSON logging
│       └── errors.py                 # ShovelsClientError, format_error
│       └── response.py               # {data, meta} envelope builder
```

## MCP Tools

### `shovels_permits`

Search U.S. building permits by `geo_id` + date range, or fetch full records by ID.

- **Search mode** (no `id`): compact rows with `resource` URI
- **Fetch mode** (`id` supplied): full permit record
- Filters: `tags`, `permit_status`, `property_type`, `min_job_value`

### `shovels_contractors`

Search contractors active in a geography, or fetch full profiles, permits, employees, or metrics.

- 5 actions via `action` param: `search`, `get`, `permits`, `employees`, `metrics`
- **Search mode**: compact rows with `resource` URI
- Filters: `contractor_classification`, `contractor_name` (min 3 chars)

### `shovels_geo`

Resolve free-text addresses/places to `geo_id`. Tries all levels — address → city → county → jurisdiction → state — with auto fallback.

- Optional `level` param to pin to one level
- Auto-corrects state name typos

### `shovels_meta`

List valid permit tags, or check current API credit usage.

- 2 actions: `tags`, `usage`

## Progressive Disclosure

Search-mode responses return **compact rows** (id, type, status, key fields + a `resource` URI). The full record is one `get` call away. This keeps token usage low — agents only pay for what they read.

| Mode                  | Payload                  | Token cost |
| --------------------- | ------------------------ | ---------- |
| Search (`no id`)      | Compact + `resource` URI | Low        |
| Fetch (`id` supplied) | Full record              | Full       |

## API Endpoints

```
GET  /health         # Service status (public, no auth)
POST /mcp            # MCP Streamable HTTP endpoint
  ├── tools/shovels_permits       # Search or fetch permits
  ├── tools/shovels_contractors   # Search or fetch contractors
  ├── tools/shovels_geo           # Resolve geo_id
  └── tools/shovels_meta          # Tags + usage
```

## Auth

All endpoints except `/health` require `X-API-Key` header — validated against the Shovels `/usage` endpoint. Each caller brings their own Shovels API key (not a single server key).

| Scenario       | Result                                 |
| -------------- | -------------------------------------- |
| No `X-API-Key` | 401 — `"Missing X-API-Key header"`     |
| Invalid key    | 401 — `"Invalid API key"`              |
| Valid key      | Passes through, tools use caller's key |
| `/health`      | Always 200 (no key needed)             |

## Environment Variables

| Variable           | Required | Default                     | Description                                                   |
| ------------------ | -------- | --------------------------- | ------------------------------------------------------------- |
| `SHOVELS_API_KEY`  | Yes      | —                           | Shovels API key (used for middleware to validate client keys) |
| `SHOVELS_API_BASE` | No       | `https://api.shovels.ai/v2` | API base URL override                                         |

## Development

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Start dev server (middleware validates keys against real Shovels API)
SHOVELS_API_KEY=sk_... uvicorn main:app --reload

# Health check (no key required)
curl https://shovels-mcp-server.onrender.com/mcp/health
```

## Known Constraints

- Free trial: **250 requests flat** (any size)
- `geo_id` + date range required for all searches
- `contractor_name` requires **3+ characters** (trigram index)
- All monetary values in **cents**
