# Shovels MCP Server

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License" />
  <img src="https://img.shields.io/badge/python-3.12+-green" alt="Python" />
  <img src="https://img.shields.io/badge/next.js-16-purple" alt="Next.js" />
</p>

<p align="center">
  <strong>Building permit intelligence, native to your AI agents.</strong><br>
  An MCP server that gives AI agents direct access to U.S. building permits,<br>contractor records, and zoning decisions — no web scraping required.
</p>

---

## Overview

Shovels is an MCP (Model Context Protocol) server wrapping the Shovels public REST API (`api.shovels.ai/v2`). Instead of exposing 15+ raw endpoints, it consolidates everything into **4 MCP tools** that AI agents (Claude Code, Cursor, etc.) can use immediately.

```
Agent (Claude/Cursor/etc.) ──MCP──▶ Shovels MCP Server ──HTTP──▶ api.shovels.ai/v2
                                        │
                                        ├── shovels_geo        → resolve places to geo_ids
                                        ├── shovels_permits    → search building permits
                                        ├── shovels_contractors→ search contractors
                                        └── shovels_meta       → tags & usage
```

## Quick Start

### 1. Get an API Key

Sign up at [app.shovels.ai](https://app.shovels.ai) for a free API key (250 requests included).

### 2. Run the Server

```bash
cd backend
pip install -r requirements.txt
SHOVELS_API_KEY=sk_... uvicorn main:app --reload
```

### 3. Configure Your Agent

Add to your MCP client config (e.g., `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "shovels": {
      "url": "http://localhost:8000",
      "headers": {
        "X-API-Key": "your-shovels-api-key"
      }
    }
  }
}
```

### 4. Start Querying

```python
# Resolve a location
shovels_geo("Austin, TX")

# Search commercial building permits
shovels_permits(geo_id="TX", permit_from="2026-01-01", permit_to="2026-06-30", property_type="commercial")

# Find electrical contractors
shovels_contractors(action="search", geo_id="CA", permit_from="2026-01-01", permit_to="2026-06-30")
```

## Architecture

```
backend/                     # Python MCP Server
├── main.py                  # FastAPI entry point
├── Dockerfile               # HuggingFace Spaces deployment
├── requirements.txt
├── src/
│   ├── config/settings.py   # Pydantic Settings
│   ├── models/              # Pydantic models
│   ├── services/            # Async HTTP client for api.shovels.ai/v2
│   ├── mcp/                 # MCP tool definitions
│   ├── api/                 # Health endpoint
│   └── utils/               # Logging, retry, errors, response formatting

frontend/                    # Next.js Marketing + Docs Site
├── app/
│   ├── (marketing)/page.tsx # Landing page
│   └── docs/                # Documentation (MDX)
├── components/              # React components + shadcn/ui
├── tailwind.config.ts       # Forest-green theme (per DESIGN.md)
└── package.json
```

## MCP Tools

| Tool | Purpose | Required Params |
|------|---------|-----------------|
| `shovels_geo` | Resolve places → geo_id | `query` |
| `shovels_permits` | Search/fetch building permits | `geo_id` + `permit_from` + `permit_to` |
| `shovels_contractors` | Search contractors, permits, employees, metrics | `geo_id` + dates (for search) |
| `shovels_meta` | List permit tags or check credit usage | `action` (tags \| usage) |

### Calling Sequence

Every query follows the same pattern:

1. **`shovels_geo("Austin, TX")`** → resolves location to a `geo_id`
2. **`shovels_permits(geo_id="...", ...)`** → search with the `geo_id`
3. (Optional) Fetch full records by ID with the `id` parameter

## Features

- **4 consolidated tools** instead of 15+ API endpoints — minimal schema bloat
- **Auto-pagination**: `limit` parameter supports `"all"` (capped at `max_records`, default 10,000)
- **Structured errors**: `{error, code, error_type}` matching CLI exit-code vocabulary
- **Rate-limit retry**: Automatic 429 retry with jitter and `Retry-After` support
- **Response compaction**: Null fields stripped from search results to reduce payload
- **Fuzzy geo matching**: State name typos auto-corrected ("Taxas" → "TX")
- **`data`/`meta` envelope**: Consistent response format across all tools
- **Credit visibility**: `credits_used` and `credits_remaining` in every response

## Development

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
SHOVELS_API_KEY=sk_... uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Opens at `http://localhost:3000`.

### Tests

```bash
cd backend
.venv/bin/python -m pytest tests/ -v
```

118 tests across unit + integration layers.

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SHOVELS_API_KEY` | Yes | — | Shovels API key (get one at app.shovels.ai) |
| `SHOVELS_API_BASE` | No | `https://api.shovels.ai/v2` | API base URL override |
| `MAX_RETRIES` | No | `3` | Network error retry count |
| `RATE_LIMIT_RETRY_MAX` | No | `5` | Max retries on HTTP 429 |
| `RATE_LIMIT_INITIAL_BACKOFF` | No | `1.0` | Initial 429 backoff in seconds |

## Known Constraints

- Free trial: **250 requests flat** (any size)
- `geo_id` + date range required for all searches
- `contractor_name` requires **3+ characters**
- `decision_q` capped at **100 characters**
- All monetary values in **cents**
- ZIP codes not supported for decisions endpoint

## Deployment

The backend is designed for HuggingFace Spaces (Docker). See `backend/Dockerfile`.

```bash
docker build -t shovels-mcp backend/
docker run -e SHOVELS_API_KEY=sk_... -p 8000:8000 shovels-mcp
```

## License

MIT
