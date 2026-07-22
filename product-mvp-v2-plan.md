# Shovels MCP Server — Technical Design
### A 1:1 mirror of the Shovels CLI's business logic, delivered over MCP instead of a shell

---

## 0. Framing

Shovels shipped a CLI instead of a public MCP server and explained why: MCP tool schemas can burn tens of thousands of tokens before real work starts, and MCP tool calls don't compose the way shell pipes do. The CLI's own landing page states this plainly — no MCP headaches, no context bloat, no credential juggling.

Composability (piping, chaining, cron jobs) is a real, permanent CLI advantage — this design doesn't try to erase it. Context bloat is not permanent — it's a consequence of *how many tools you expose and how much you return per call*, and it's fixable without touching business logic at all.

**The rule this design follows: change nothing about what the tools do or how they behave. Change only how many there are and how much each response carries.** Every flag, default, output field, and error code below is taken directly from the CLI's own README (`ShovelsAI/shovels-cli`, MIT licensed, Go/Cobra) — not reinvented.

---

## 1. What the CLI actually provides (the thing being mirrored)

```
shovels
├── permits
│   ├── search      Search building permits by location, date, type, value
│   └── get         Retrieve one or more permits by ID (1–50 IDs)
├── contractors
│   ├── search      Search contractors by location and filters
│   ├── get         Retrieve one or more contractors by ID
│   ├── permits     List permits filed by a contractor
│   ├── employees   List employees of a contractor
│   └── metrics     Monthly performance metrics for a contractor
├── addresses
│   └── search      Search addresses by street, city, state, or zip
├── cities
│   └── search      Resolve city names to geo_ids
├── counties
│   └── search      Resolve county names to geo_ids
├── jurisdictions
│   └── search      Resolve jurisdiction names to geo_ids
├── tags
│   └── list        List valid permit tag values
└── usage           Show current API credit usage
```

Not wrapped by the CLI, and therefore **out of scope for a faithful mirror**: `/decisions/search` exists in the public API but has no CLI command. Adding it would be scope creep beyond "same as CLI," so it's excluded from this MVP — flagged here so it's a deliberate choice, not an oversight, if you later decide to add it.

### Output contract (verbatim from the CLI)

Paginated:
```json
{
  "data": [ ... ],
  "meta": { "count": 25, "has_more": true, "credits_used": 1, "credits_remaining": 9999 }
}
```
Single object:
```json
{
  "data": { ... },
  "meta": { "credits_used": 1, "credits_remaining": 9999 }
}
```
Error:
```json
{ "error": "...", "code": 2, "error_type": "auth_error" }
```
`error_type` values: `client_error`, `validation_error`, `auth_error`, `rate_limited`, `credit_exhausted`, `server_error`, `network_error` — mapping to exit codes 1–5 in the CLI, which become MCP tool error payloads here (no shell exit code to carry, so `code`/`error_type` ride along in the JSON error instead).

### Pagination & global behavior (verbatim)

- `--limit`: 1–100000 or `all` (default 50)
- `--max-records`: cap for `limit=all`, default 10000, hard ceiling 100000
- `--no-retry`: disable 429 backoff (default: retry with jitter, respects `Retry-After`)
- `--timeout`: per-request timeout, default 30s

The MCP server reproduces this exactly: `limit`/`max_records` params with the same defaults and ceilings, automatic retry-with-jitter on 429 unless disabled, same timeout default.

---

## 2. The one thing that changes: tool count and payload shape

11 subcommands mirrored 1:1 as 11 MCP tools reproduces the exact schema-bloat problem the CLI post complains about. So subcommands are grouped under 4 tools by resource family, routed internally by an `action` (or presence of `id`) parameter — every underlying subcommand's flags, defaults, and output are preserved untouched inside that routing.

| MCP tool | Mirrors | Routing |
|---|---|---|
| `shovels_permits` | `permits search`, `permits get` | `id` present → get; absent → search |
| `shovels_contractors` | `contractors search/get/permits/employees/metrics` | `action`: `search`\|`get`\|`permits`\|`employees`\|`metrics` |
| `shovels_geo` | `addresses/cities/counties/jurisdictions search` | `level`: `address`\|`city`\|`county`\|`jurisdiction` |
| `shovels_meta` | `tags list`, `usage` | `action`: `tags`\|`usage` |

Second lever, additive and separable from the first: **search-mode responses return compact rows + a resource pointer, not the full record** — full detail is one `get` call away, same as the CLI's own `search` → `get` split already implies (you already have to know an ID to `get` it; this just means the search step doesn't have to hand you every field of every row to make that possible). This is the resource-links pattern from the MCP spec, applied without changing what `search` or `get` return in substance — only how much of it rides on the wire when it isn't needed yet.

---

## 3. Full tool specs

### `shovels_permits`

```json
{
  "name": "shovels_permits",
  "description": "Search building permits by location, date, type, value; or fetch full records by ID. Mirrors `shovels permits search` / `shovels permits get`.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "id": { "type": "array", "items": {"type": "string"}, "maxItems": 50, "description": "1-50 permit IDs. Present = get mode." },
      "geo_id": { "type": "string", "description": "Required for search. Zip, state code, or geo_id from shovels_geo." },
      "permit_from": { "type": "string", "format": "date", "description": "Required for search." },
      "permit_to": { "type": "string", "format": "date", "description": "Required for search." },
      "tags": { "type": "array", "items": {"type": "string"}, "description": "Prefix '-' to exclude. AND logic across multiple tags." },
      "property_type": { "type": "string" },
      "min_job_value": { "type": "integer", "description": "Cents." },
      "include_count": { "type": "boolean", "default": false },
      "limit": { "type": "string", "default": "50", "description": "1-100000 or 'all'." },
      "max_records": { "type": "integer", "default": 10000, "maximum": 100000 }
    }
  },
  "annotations": { "readOnlyHint": true }
}
```

### `shovels_contractors`

```json
{
  "name": "shovels_contractors",
  "description": "Search/fetch contractors, their permits, employees, or monthly metrics. Mirrors `shovels contractors search/get/permits/employees/metrics`.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "action": { "type": "string", "enum": ["search", "get", "permits", "employees", "metrics"], "default": "search" },
      "id": { "type": "array", "items": {"type": "string"}, "description": "Contractor ID(s). Required for get/permits/employees/metrics." },
      "geo_id": { "type": "string", "description": "Required for action=search." },
      "permit_from": { "type": "string", "format": "date" },
      "permit_to": { "type": "string", "format": "date" },
      "contractor_classification": { "type": "string" },
      "metric_from": { "type": "string", "format": "date", "description": "Required for action=metrics." },
      "metric_to": { "type": "string", "format": "date", "description": "Required for action=metrics." },
      "property_type": { "type": "string", "description": "Required for action=metrics." },
      "tag": { "type": "string", "description": "Required for action=metrics." },
      "include_count": { "type": "boolean", "default": false },
      "limit": { "type": "string", "default": "50" },
      "max_records": { "type": "integer", "default": 10000, "maximum": 100000 }
    }
  },
  "annotations": { "readOnlyHint": true }
}
```

### `shovels_geo`

```json
{
  "name": "shovels_geo",
  "description": "Resolve free-text place names to Shovels geo_ids for use in geo_id params elsewhere. Mirrors `shovels addresses/cities/counties/jurisdictions search`.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string", "description": "Free-text address, city, county, or jurisdiction name." },
      "level": { "type": "string", "enum": ["address", "city", "county", "jurisdiction"], "default": "address" },
      "limit": { "type": "string", "default": "50" }
    },
    "required": ["query"]
  },
  "annotations": { "readOnlyHint": true }
}
```

### `shovels_meta`

```json
{
  "name": "shovels_meta",
  "description": "List valid permit tags, or check current API credit usage. Mirrors `shovels tags list` / `shovels usage`.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "action": { "type": "string", "enum": ["tags", "usage"], "default": "usage" },
      "limit": { "type": "string", "default": "50", "description": "Only used for action=tags." }
    }
  },
  "annotations": { "readOnlyHint": true }
}
```

---

## 4. Response shapes

Search mode (`shovels_permits`, no `id`) — compact rows, same `data`/`meta` envelope as the CLI, full detail one `get` call away:

```json
{
  "data": [
    {
      "id": "caf3b9d5ce317d53",
      "number": "RE2303928",
      "type": "electrical - 1 & 2 unit residential",
      "status": "active",
      "job_value_cents": 500000,
      "city": "OAKLAND", "state": "CA",
      "contractor_id": "KOm4dMLIuT"
    }
  ],
  "meta": { "count": 1, "has_more": true, "credits_used": 1, "credits_remaining": 9999 }
}
```

Get mode (`id` supplied) — full record, same shape as CLI `permits get`, single object per requested ID.

Errors — identical shape and `error_type` vocabulary to the CLI, `code` carried as data instead of a shell exit code:

```json
{ "error": "Rate limited, retry after backoff", "code": 3, "error_type": "rate_limited" }
```

---

## 5. What's identical to the CLI (the "solved" part is additive, not a rewrite)

- Same 4 credential/auth model: `X-API-Key` header, same key works in both.
- Same pagination semantics: `limit`, `max_records`, `has_more`, cursor handling internal either way.
- Same retry behavior: backoff + jitter on 429, respects `Retry-After`, toggleable.
- Same error vocabulary: `error_type` values carried through unchanged.
- Same credit visibility: `credits_used` / `credits_remaining` on every response.
- Same scope: no Decisions tool, since the CLI doesn't have one either.

## 6. What's different (the fix, isolated to exactly two things)

1. **11 subcommands → 4 tools**, routed by `action`/`id` params instead of separate tool names — cuts schema tokens loaded per session roughly proportional to tool count.
2. **Search responses return compact rows + let `get` fetch full detail**, instead of full payload on every row — cuts per-call token cost independent of how many fields the underlying record has.

Both are additive to the existing CLI design, not replacements for it — an agent that already knows the CLI's field names and flag semantics needs to learn almost nothing new to use this.

---

## 7. Build plan

1. Get a free API key (`app.shovels.ai/create-account`, 250 free requests).
2. Build 4 tools as a thin wrapper (FastMCP/Python or `@modelcontextprotocol/sdk`/TS) — each is an HTTP call to `api.shovels.ai/v2` + the shape transform above. No new business logic to invent; port the CLI's Go request-building and retry logic directly.
3. Reproduce global behavior once, shared across all 4 tools: retry-with-jitter, `limit`/`max_records` handling, `credits_remaining` surfacing.
4. Test in Claude Desktop against real responses.
5. Pitch framing: *"Same tool your CLI already validated, same flags, same output contract — delivered over MCP for the clients that can't shell out, with the two specific things your CLI post flagged about MCP fixed."*

---

*Grounded in `ShovelsAI/shovels-cli` (MIT, public GitHub repo) and `docs.shovels.ai` as of July 2026. Verify against the live repo/spec before shipping — both can change.*