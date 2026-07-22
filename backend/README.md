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

An MCP (Model Context Protocol) server wrapping the [Shovels public API](https://api.shovels.ai/v2) — search U.S. building permits, contractors, and geo-resolve locations.

A 1:1 mirror of the Shovels CLI's business logic, delivered over MCP instead of a shell. Built with **progressive disclosure**: search returns compact rows + `resource` URIs; fetch-by-ID returns full records.

## Tools

| Tool | What it does | Modes |
|---|---|---|
| `shovels_permits` | Search permits by geo + date range, or fetch full records by ID | search (compact), get-by-ID (full) |
| `shovels_contractors` | Search contractors, or fetch profiles, permits, employees, metrics | 5 actions: search, get, permits, employees, metrics |
| `shovels_geo` | Resolve free-text place names to `geo_id` values | Level-pin or auto-fallback |
| `shovels_meta` | List valid permit tags, or check API credit usage | tags, usage |

### Progressive Disclosure

Search responses return compact rows with a `resource` pointer (e.g. `shovels://permits/<id>`). Agents fetch the full record only when needed — keeping token usage low.

## Quick Start

```bash
# 1. Get a free API key at https://app.shovels.ai/create-account
# 2. Set your key
export SHOVELS_API_KEY=sk_...

# 3. Start the server
cd backend
uvicorn main:app --reload

# 4. Health check (no key required)
curl http://localhost:8000/health
```

## Auth

All endpoints except `/health` require `X-API-Key` header. Keys are validated against the Shovels `/usage` endpoint. Each client brings their own key.

| Scenario | Result |
|---|---|
| No `X-API-Key` | 401 |
| Invalid key | 401 |
| Valid key | Passes through |
| `/health` | Always 200 |

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SHOVELS_API_KEY` | Yes | Your Shovels API key |
| `SHOVELS_API_BASE` | No | API base URL (default: `https://api.shovels.ai/v2`) |

## Architecture

- **Framework**: FastAPI + FastMCP
- **Transport**: MCP Streamable HTTP
- **Deployment**: HuggingFace Spaces (Docker)

No database, no vector store, no frontend — just a thin proxy to the Shovels REST API with retry logic, credit-header surfacing, and key validation.

## Known Constraints

- Free trial: **250 requests** (flat, any size)
- `geo_id` + date range are **required** for search
- `contractor_name` requires **3+ characters** (trigram index)
- Job values, fees, market values are in **cents**
