---
title: Shovels MCP Server
emoji: 🏗️
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Shovels MCP Server

An MCP (Model Context Protocol) server wrapping the [Shovels public API](https://api.shovels.ai/v2) — search U.S. building permits, contractors, and zoning/land-use decisions.

Built as a lightweight HTTP proxy: 4 consolidated MCP tools instead of 15+ raw API endpoints.

## Tools

| Tool | What it does |
|---|---|
| `shovels_permits` | Search permits by geo + date range, or fetch full records by ID |
| `shovels_contractors` | Search contractors by geo + date range, or fetch full profiles by ID |
| `shovels_decisions` | Search zoning/land-use decisions by geo + date range, or fetch full records by ID |
| `shovels_geo` | Resolve free-text place names to `geo_id` values (required before other searches) |

### Progressive Disclosure

- **Search mode** (no `id`): compact rows with a `resource` URI pointing to more detail
- **Fetch mode** (`id` supplied): the full record

This keeps token usage low — agents only pay for what they read.

## Quick Start

```bash
# 1. Get a free API key at https://app.shovels.ai/create-account
# 2. Set your key
export SHOVELS_API_KEY=sk_...

# 3. Start the server
cd backend
uvicorn main:app --reload

# 4. Test it
curl http://localhost:8000/health
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SHOVELS_API_KEY` | Yes | Your Shovels API key |
| `SHOVELS_API_BASE` | No | API base URL (default: `https://api.shovels.ai/v2`) |

## Architecture

- **Framework**: FastAPI + FastMCP
- **Transport**: MCP Streamable HTTP
- **Deployment**: HuggingFace Spaces (Docker)

No database, no vector store, no frontend — just a thin proxy to the Shovels REST API with retry logic and credit-header surfacing.

## Known Constraints

- Free trial: **250 requests** (flat, any size)
- `geo_id` + `permit_from`/`permit_to` (or `decision_from`/`decision_to`) are **required** for search
- `contractor_name` requires **3+ characters** (trigram index)
- `decision_q` capped at **100 characters**
- Decisions: **ZIP code filtering not supported**
- Job values, fees, market values are in **cents**
