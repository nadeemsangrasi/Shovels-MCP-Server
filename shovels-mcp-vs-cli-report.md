# Shovels MCP Server — Addressing the Shovels Team's MCP Concerns

> **Context:** Shovels built a CLI rather than an MCP server because they identified
> specific problems with the MCP approach. This report analyzes how the Shovels MCP
> Server addresses (or doesn't) each of those concerns.
>
> Source: [`shoverls-issues-for-mcp.md`](shoverls-issues-for-mcp.md)
>
> **Live deploy:** `https://shovels-mcp-server.onrender.com/mcp`
> **Repo:** [your-github-link]

---

## The 7 Concerns — Addressed

### 1. Token Overhead (Progressive Disclosure)

**The concern:** *"Tool schema definitions alone can consume tens of thousands of tokens
before any real work begins. One benchmark found CLI-based agents had 95% of their
context window free for actual reasoning."*

**Status: ✅ Solved — via MCP Resources**

**What the server does:**

- **Compact search results** — `_compact_permit()`, `_compact_contractor()`
  reduce full records (23+ fields) to 7 key fields including a `resource` URI.
  [tools.py lines 77-132]

- **`_strip_nulls()`** — recursively removes `null` values from payloads, further
  shrinking every response. [tools.py lines 68-74]

- **Progressive disclosure via MCP Resources** — the `resource` field is NOT just text,
  it's a registered MCP Resource Template that agents read natively:

| Step | How | Fields | Schema Cost |
|------|-----|--------|-------------|
| Search | `shovels_permits(geo_id="CA", ...)` | **7 fields** (compact) | ~900 tokens (tool schema) |
| Drill-down | `read_resource("shovels://permits/{id}")` | **23 fields** (full) | **~5 tokens** (just the URI) |

**Verified on production:**
```
Search:   id, number, type, status, city, state, resource  (7 fields)
Resource: property_*, address, tags, dates, geo_ids...      (23 fields)
```

**Token savings:** ~71% on search responses, ~99% on drill-down (no tool schema reload).

**Registered Resource Templates:**
```
shovels://permits/{permit_id}       → get_permit_resource()
shovels://contractors/{contractor_id} → get_contractor_resource()
```

**Code proof — compact search result:**  `tools.py lines 77-101`
```python
def _compact_permit(item: dict) -> dict:
    return _strip_nulls({
        "id": item.get("id"),
        "number": item.get("number"),
        "type": item.get("type"),
        "status": item.get("status"),
        "city": ...,
        "state": ...,
        "resource": f"shovels://permits/{item.get('id')}",
    })
```

**Code proof — Resource handler:** `tools.py lines 630-645`
```python
@mcp.resource("shovels://permits/{permit_id}")
async def get_permit_resource(permit_id: str) -> dict:
    client = get_client()
    result = await client.get_permits([permit_id])
    return _build_single_envelope(result)
```

---

### 2. Pagination (No More Loops)

**The concern:** *"No more pagination loops. The CLI handles cursor management and
pagination automatically."*

**Status: ✅ Solved**

**What the server does:**

- Every search response includes `meta.cursor` when more pages exist.
  The agent passes this back as `cursor` to fetch the next page — no loop logic
  needed. [tools.py line 262; response.py line 47]

- `limit` parameter supports values 1-100 (default 50). [tools.py lines 225-244]

**Response shape:**
```json
{
  "data": [ /* compact items */ ],
  "meta": {
    "count": 47,
    "has_more": true,
    "cursor": "next_page_token",
    "credits_used": 1,
    "credits_remaining": 249
  }
}
```

**Agent flow:**
```
Call 1: shovels_permits(geo_id="CA", ...)  → meta.cursor = "abc"
Call 2: shovels_permits(geo_id="CA", cursor="abc") → meta.cursor = "def"
Call 3: shovels_permits(geo_id="CA", cursor="def") → meta.has_more = false
```

---

### 3. Rate Limiting (Built-in Retry)

**The concern:** *"Rate limiting is handled automatically with exponential backoff."*

**Status: ✅ Solved**

**What the server does:**

Two independent retry loops in `ShovelsClient._request()` [shovels_client.py lines 66-128]:

| Error Type | Max Retries | Backoff | Jitter |
|---|---|---|---|
| HTTP 429 (rate limit) | 5 (configurable) | 1s → 2s → 4s → 8s → 16s (capped at 60s) | ±25% + Retry-After support |
| Network errors | 3 (configurable) | 2s → 4s → 8s | None |

- `no_retry` flag on every tool for agents that want to handle it themselves.
- Respects HTTP `Retry-After` header. [shovels_client.py lines 99-101]
- HTTP 429 + `credits_remaining=0` → promoted to `credit_exhausted`. [errors.py lines 69-70]

---

### 4. Counts (Always Know the Scope)

**The concern:** *"Every query returns the total count of matching records (up to 10,000)."*

**Status: ✅ Solved**

**What the server does:**

- `meta.count` on every search response. [response.py line 40]
- `include_count` parameter forwards to Shovels API for exact totals. [tools.py lines 358-359]
- `meta.has_more` indicates additional pages. [response.py line 42]

---

### 5. Credit Tracking (Always Know the Cost)

**The concern:** *"Every result includes how many credits you used and how many you have left."*

**Status: ✅ Solved**

**What the server does:**

- `_extract_credits()` reads `X-Credits-*` headers from every API response.
  [shovels_client.py lines 43-50]
- `meta.credits_used` and `meta.credits_remaining` on **every single response**.
  [tools.py lines 252-254]
- Dedicated `shovels_meta(action="usage")` tool. [tools.py lines 596-602]
- HTTP 402 (credit exhausted) detected in middleware with clear upgrade URL.
  [main.py lines 119-132]

**Error on credit exhaustion:**
```json
{
  "error": "credit_exhausted",
  "code": 3,
  "message": "Trial credit limit reached. Upgrade at https://pay.shovels.ai/..."
}
```

---

### 6. Agent-Friendly Output

**The concern:** *"JSON to stdout. Errors to stderr. Meaningful exit codes."*

**Status: ✅ Solved**

**What the server does:**

- **Consistent `{data, meta}` envelope** on every response. [response.py lines 11-57]
- **Structured error codes** matching CLI exit-code vocabulary exactly. [errors.py lines 30-37]

| HTTP Status | `error_type` | `code` | CLI Equivalent |
|---|---|---|---|
| 400 / 404 | `client_error` | 1 | exit code 1 |
| 401 / 403 | `auth_error` | 2 | exit code 2 |
| 402 | `credit_exhausted` | 3 | exit code 3 |
| 429 | `rate_limited` | 3 | exit code 3 |
| 500+ | `server_error` | 4 | exit code 4 |
| Network error | `network_error` | 5 | exit code 5 |

- No raw exceptions leak — every tool wraps calls in try/except `ShovelsClientError`.
  [tools.py lines 325-330]

---

### 7. CLI Composability

**The concern:** *"A CLI agent can pipe outputs, chain commands, and filter results
at the shell level in ways that MCP tool calls don't naturally support."*

**Status: ⚠️ Architectural — not solvable at the MCP protocol level**

**Why this is different:**

| Capability | CLI | MCP |
|---|---|---|
| Pipe / chain | `shovels permits \| jq` | Structured function calls |
| Filter results | `grep`, `jq` at shell level | Parameters in tool schema |
| Compose tools | Shell scripts / `xargs` | Agent calls tools sequentially |

This is a fundamental protocol difference — the same reason AWS ships `aws` CLI and
Google ships `gcloud` CLI rather than MCP servers. The CLI is better for shell-level
automation; MCP is better for standardized access across AI clients (Claude Desktop,
VS Code, Cursor). They complement each other.

**Mitigations in place:**
- Geo-resolution as prerequisite → natural search pipeline
- Cursor chaining in every response → loop-free pagination
- MCP Resource URIs → protocol-native drill-down without tool schema reload

---

## Summary

| # | Concern | Status | Key Technique |
|---|---------|--------|--------------|
| 1 | Token overhead | ✅ **Solved** | Compact records (7 fields) + MCP Resources (23 fields) + `_strip_nulls()` |
| 2 | Pagination loops | ✅ **Solved** | `meta.cursor` in every response, pass back to get next page |
| 3 | Rate limiting | ✅ **Solved** | Exponential backoff + jitter + Retry-After, 5 retries, configurable |
| 4 | Counts | ✅ **Solved** | `meta.count` + `include_count` for totals up to 10,000 |
| 5 | Credit tracking | ✅ **Solved** | Credits on every response + dedicated usage tool + HTTP 402 handling |
| 6 | Agent-friendly output | ✅ **Solved** | `{data, meta}` envelope + CLI-matching error codes (1-5) |
| 7 | CLI composability | ⚠️ **Inherent** | Protocol-level difference — same reason AWS ships `aws` CLI, not an MCP server |

**6 of 7 concerns solved.** The 7th is a protocol tradeoff, not a solvable bug.

---

## Live Demo

- Deployed: `https://shovels-mcp-server.onrender.com/mcp`
- Try it: Any Shovels API key → `resources/templates/list` → `tools/call` → `resources/read`

**Quick test:**
```bash
# Search (compact — 7 fields)
curl -X POST https://shovels-mcp-server.onrender.com/mcp \
  -H "X-API-Key: YOUR_KEY" -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"shovels_permits","arguments":{"geo_id":"CA","permit_from":"2026-07-01","permit_to":"2026-07-23","limit":"2"}}}'

# Read resource (full — 23 fields, no tool schema)
curl -X POST https://shovels-mcp-server.onrender.com/mcp \
  -H "X-API-Key: YOUR_KEY" -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":2,"method":"resources/read","params":{"uri":"shovels://permits/{id}"}}'
```
