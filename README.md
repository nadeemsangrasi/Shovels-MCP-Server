# 🏗️ Shovels MCP Server

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License" />
  <img src="https://img.shields.io/badge/python-3.12+-green" alt="Python" />
  <img src="https://img.shields.io/badge/next.js-16-purple" alt="Next.js" />
  <img src="https://img.shields.io/badge/tests-123_✔️-brightgreen" alt="Tests" />
  <img src="https://img.shields.io/badge/MCP-server-8A2BE2" alt="MCP" />
</p>

An MCP (Model Context Protocol) server that gives AI agents direct access to U.S. building permits, contractor records, and property data via the Shovels API.

Built with **progressive disclosure** — search returns compact results, full records on demand via MCP Resources. No tool schema reload, just a URI.

**Live server:** `https://shovels-mcp-server.onrender.com/mcp`

---

## Quick Start

### 1. Get an API Key

Sign up at [app.shovels.ai](https://app.shovels.ai) for a free key (250 requests included).

### 2. Configure Your Agent

Add to your MCP client config (`claude_desktop_config.json` or `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "shovels": {
      "url": "https://shovels-mcp-server.onrender.com/mcp",
      "headers": { "X-API-Key": "your-shovels-api-key" }
    }
  }
}
```

### 3. Search Permits

```python
# Resolve a location
shovels_geo("Austin, TX")

# Search permits
shovels_permits(geo_id="a4xysKbZwqg", permit_from="2026-01-01", permit_to="2026-06-30", limit="10")
```

---

## Tools

| Tool | What it does | Key Params |
|------|-------------|------------|
| `shovels_geo` | Resolve places to geo_ids | `query` (address, city, state) |
| `shovels_permits` | Search/fetch permits | `geo_id` + dates (search) / `id` (fetch) |
| `shovels_contractors` | Search contractors, permits, employees, metrics | `action` + `geo_id` + dates (search) / `id` (get) |
| `shovels_meta` | List permit tags or check credit usage | `action` (`tags` or `usage`) |

### Calling Sequence

```
1. shovels_geo("Austin, TX")           → geo_id  ──┐
2. shovels_permits(geo_id=..., ...)     ←──────────┘
3. read_resource("shovels://permits/{id}")  → full record (no schema reload)
```

### Full Parameter Tables

<details>
<summary>shovels_permits — 12 parameters</summary>

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | `list[str]` | For fetch | 1-50 permit IDs |
| `geo_id` | `string` | For search | From `shovels_geo` |
| `permit_from` | `string` | For search | YYYY-MM-DD |
| `permit_to` | `string` | For search | YYYY-MM-DD |
| `tags` | `list[str]` | No | `solar`, `hvac`, `new_construction`, etc. |
| `permit_status` | `list[str]` | No | `final`, `in_review`, `active`, `inactive` |
| `property_type` | `string` | No | `commercial`, `residential`, `industrial` |
| `min_job_value` | `int` | No | Minimum in cents |
| `cursor` | `string` | No | Pagination cursor |
| `include_count` | `bool` | No | Request total count |
| `limit` | `string` | No | 1-100 (default `"50"`) |
| `no_retry` | `bool` | No | Disable 429 retry |

</details>

<details>
<summary>shovels_contractors — 5 actions</summary>

| Action | Required Params | Returns |
|--------|----------------|---------|
| `search` | `geo_id` + `permit_from` + `permit_to` | Compact contractor list |
| `get` | `id` | Full profile (21 fields) |
| `permits` | `id` + `geo_id` + dates | Permits filed by contractor |
| `employees` | `id` | Employee list |
| `metrics` | `id` + dates + `property_type` + `tag` | Monthly metrics |

</details>

---

## Resources (Progressive Disclosure)

Search results include `"resource": "shovels://permits/{id}"` — a real MCP Resource, not just text. Agents read it directly without loading the tool schema.

| Resource URI | Returns |
|-------------|---------|
| `shovels://permits/{permit_id}` | 23+ fields (address, tags, dates, property details, geo_ids) |
| `shovels://contractors/{contractor_id}` | 21+ fields (name, phone, email, rating, permit_count, total_job_value) |

**Token savings:** Search returns 7 compact fields (~70% less than full). Resource read costs ~5 tokens vs ~900 for a tool call (~99% less).

---

## Response Format

All responses use a consistent `{data, meta}` envelope with credit info on every call.

```json
// Search success — compact items + pagination + credits
{ "data": [{ "id": "...", "type": "...", "resource": "shovels://permits/..." }],
  "meta": { "count": 3, "has_more": true, "cursor": "...", "credits_used": 3, "credits_remaining": 247 } }

// Error — typed with CLI-matching code
{ "error": "geo_id is required...", "code": 4, "error_type": "server_error" }
```

Error codes map 1:1 to the Shovels CLI: `client_error=1`, `auth_error=2`, `rate_limited/credit_exhausted=3`, `server_error=4`, `network_error=5`.

---

## Run Locally

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
SHOVELS_API_KEY=sk_... uvicorn main:app --reload --port 8000
```

Or Docker:

```bash
cd backend && docker build -t shovels-mcp-server .
docker run -e SHOVELS_API_KEY=sk_... -p 7860:7860 shovels-mcp-server
```

Environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SHOVELS_API_KEY` | Yes | — | Your Shovels API key |
| `SHOVELS_API_BASE` | No | `https://api.shovels.ai/v2` | API base URL |
| `RATE_LIMIT_RETRY_MAX` | No | `5` | Max 429 retries |
| `MAX_RETRIES` | No | `3` | Network error retries |

---

## Architecture

```
backend/                     # Python MCP Server (FastAPI + FastMCP)
├── main.py                  # Entry point + API key middleware
├── Dockerfile               # Docker image
├── src/
│   ├── mcp/tools.py         # 4 tools + 2 Resources
│   ├── services/            # HTTP client (retry, pagination, credits)
│   └── utils/               # Error codes, response envelope, logging
└── tests/                   # 123 tests (unit + integration)

frontend/                    # Next.js 16 marketing + docs site
├── app/(marketing)/page.tsx # Landing page
├── app/docs/               # MDX documentation
└── components/              # shadcn/ui + custom components
```

---

## Testing

```bash
cd backend && .venv/bin/python -m pytest tests/ -v --cov=src
```

123 tests, ~88% coverage. Tests cover client retry logic, tool validation, resource handlers, auth middleware, and health endpoint.

---

## Contributing

This project is open source. PRs welcome.

1. Fork the repo
2. Create a feature branch
3. Make changes with tests
4. Run `pytest tests/ -v` — all must pass
5. Open a PR

---

## Deployment

One-click deploy on Render from the repo. Or manually:

```bash
cd backend
docker build -t shovels-mcp-server .
docker run -e SHOVELS_API_KEY=sk_... -p 7860:7860 shovels-mcp-server
```

---

## Known Constraints

- **Free trial:** 250 requests flat. Upgrade at [pay.shovels.ai](https://pay.shovels.ai)
- **`geo_id` + date range** required for all searches
- **`contractor_name`** requires 3+ characters (trigram index)
- **All monetary values** in cents
- **Pagination** capped at 100 records per page

---

## License

MIT

---

## Links

- **Live server:** https://shovels-mcp-server.onrender.com
- **API docs:** https://docs.shovels.ai
- **Get a key:** https://app.shovels.ai
