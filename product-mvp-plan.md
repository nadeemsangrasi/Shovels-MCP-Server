# An MCP Server for the Shovels API
### An external, unofficial build — proposed to the Shovels team as a pitch

---

## Part 1 — The Pitch

### 1. What this is

Shovels doesn't ship a public MCP server. They ship a public **REST API** (`api.shovels.ai/v2`) and a **CLI**. Their own CLI launch post makes the case against a public MCP server: tool schema definitions alone can consume tens of thousands of tokens before any real work begins, and MCP tool calls don't naturally support the pipe/chain/filter composability a CLI gives an agent.

That's a real cost — but it's a cost of a specific *design pattern* (many granular tools, full payloads every time), not of MCP itself. This proposal is a working MCP server, built entirely against their **public** API (no inside access needed), that sidesteps that cost through consolidation and lazy loading — then pitched to Shovels as a reference implementation of the MCP server they didn't think was worth building yet.

### 2. What I actually found in their docs (grounding, not guesswork)

- Public API surface: **Permits**, **Contractors**, **Decisions**, plus geo-resolution endpoints for **Addresses, Cities, Counties, Jurisdictions, States**. There is *no* public Properties endpoint — property fields (type, lot size, market value, etc.) are embedded inside permit and decision records only.
- Auth: single header, `X-API-Key: YOUR_API_KEY_HERE`. No OAuth flow to build.
- Every search endpoint requires a `geo_id` — and explicitly **rejects free-text addresses** ("123 Main St" is not accepted). You must resolve text → `geo_id` first via the Addresses/Cities/Counties/Jurisdictions search endpoints. This is the connective tissue of the whole API.
- Pagination is cursor-based: `{ items, size, next_cursor }`, plus an `include_count` flag for an exact-or-capped total.
- Billing: free trial = 250 requests flat (any size). Paid plans = credit-per-record (a 100-result search cost 100 credits). Every response carries `X-Credits-Request` / `X-Credits-Limit` / `X-Credits-Remaining` headers — a server can surface this to the agent for free.
- Rate limits are enforced individually/informally (429 on abuse), no published numbers — so client-side backoff matters.

### 3. Why 4 tools, not the ~10+ endpoints in their spec

Their spec has a search + by-ID + metrics endpoint for each of Permits, Contractors, Decisions, plus separate search endpoints for Addresses, Cities, Counties, Jurisdictions, States. Mapped 1:1 to MCP tools, that's 15+ tools — exactly the schema-bloat problem their CLI post complains about.

Consolidation:

| Tool | Wraps | Behavior |
|---|---|---|
| `shovels_permits` | `/permits/search`, `/permits/{id}` | `id` param present → fetch; absent → search |
| `shovels_contractors` | `/contractors/search`, `/contractors/{id}` | same pattern |
| `shovels_decisions` | `/decisions/search`, `/decisions/{id}` | same pattern |
| `shovels_geo` | `/addresses/search`, `/cities/search`, `/counties/search`, `/jurisdictions/search`, `/states/search` | one `query` + optional `level` param routes to the right endpoint; returns `geo_id`s |

City/county/jurisdiction/state *metrics* endpoints and the `/lists` and `/meta` endpoints are left out of the MVP — they're low-frequency, and an agent that needs them can be told to hit the CLI or API directly. Keeping the MVP at 4 is the whole point.

### 4. The progressive-disclosure part

Their `PermitsRead`/`ContractorsRead`/`DecisionsRead` objects are wide — permits alone carry 9 property-related fields, timing/duration fields, tags, embedded address, embedded geo_ids. Returning that in full for every row of a 50-result search is exactly the token cost their post is worried about.

So `shovels_permits` (and the others) return two shapes depending on whether `id` was passed:

- **Search mode**: compact rows — `id`, `number`, `type`, `status`, `job_value`, `address.city`/`state`, `contractor_id` — plus a `resource` URI. Full record is one field short of "click for more."
- **Fetch mode** (`id` supplied): the full record, since the agent explicitly asked for it.

This is the same lever the June 2025 MCP spec update (resource links) formalized — tool responses can point at more detail instead of embedding it, so context cost tracks what the agent actually reads, not what's theoretically available.

### 5. Handling credits/pagination/rate-limits *for* the agent

This is where an MCP wrapper beats both raw API and CLI for a GUI-client user (Claude Desktop, a future shovels.ai chat widget, etc.):

- Server manages `cursor` internally across a conversation; the agent asks for "more results," not "the cursor from three tool calls ago."
- Every tool response includes a `credits_remaining` field pulled from the `X-Credits-Remaining` header, so the agent can warn the user before they blow through a trial key.
- 429s get retried with backoff inside the server, invisible to the agent — one fewer thing the model has to reason about or get wrong.

### 6. Positioning this as a pitch to Shovels

The honest framing: *"You explained why you built a CLI instead of a public MCP server — here's a working MCP server against your public API that answers those specific concerns, as a reference implementation."* That's a concrete artifact, not a cold pitch. It demonstrates the API deeply enough to be useful evidence for a contributor/hire conversation, without needing any access you don't already have as a developer with an API key.

---

## Part 2 — Detailed Spec (Appendix)

### A. Tool schemas

```json
{
  "name": "shovels_permits",
  "description": "Search U.S. building permits by geo_id, date range, tags, job value, contractor classification, or property attributes. Supply `id` (one or more) to fetch full permit records instead of searching.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "id": { "type": "array", "items": { "type": "string" }, "description": "One or more permit IDs — fetch full records instead of searching" },
      "geo_id": { "type": "string", "description": "Required for search mode. State code, ZIP, or a geo_id from shovels_geo." },
      "permit_from": { "type": "string", "format": "date", "description": "Required for search mode." },
      "permit_to": { "type": "string", "format": "date", "description": "Required for search mode." },
      "permit_tags": { "type": "array", "items": { "type": "string" }, "description": "Prefix with '-' to exclude, e.g. '-roofing'." },
      "permit_status": { "type": "array", "items": { "type": "string", "enum": ["final", "in_review", "inactive", "active"] } },
      "permit_min_job_value": { "type": "integer", "description": "Cents." },
      "contractor_classification_derived": { "type": "array", "items": { "type": "string" } },
      "cursor": { "type": "string", "description": "Omit for first page; server can also manage this internally across a session." },
      "size": { "type": "integer", "default": 20, "maximum": 100 }
    }
  },
  "annotations": { "readOnlyHint": true }
}
```

```json
{
  "name": "shovels_contractors",
  "description": "Search contractors active in a geography, filtered by trade classification, license, or job history. Supply `id` (one or more) to fetch full contractor profiles.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "id": { "type": "array", "items": { "type": "string" } },
      "geo_id": { "type": "string", "description": "Required for search mode." },
      "permit_from": { "type": "string", "format": "date", "description": "Required for search mode." },
      "permit_to": { "type": "string", "format": "date", "description": "Required for search mode." },
      "contractor_classification_derived": { "type": "array", "items": { "type": "string" } },
      "contractor_name": { "type": "string", "minLength": 3 },
      "contractor_min_total_job_value": { "type": "integer" },
      "cursor": { "type": "string" },
      "size": { "type": "integer", "default": 20, "maximum": 100 }
    }
  },
  "annotations": { "readOnlyHint": true }
}
```

```json
{
  "name": "shovels_decisions",
  "description": "Search local zoning/land-use decisions (rezonings, variances) by geo_id and date range. Supply `id` (one or more, up to 50) to fetch full decision records.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "id": { "type": "array", "items": { "type": "string" }, "maxItems": 50 },
      "geo_id": { "type": "string", "description": "Required for search mode. State or place geo_id only — ZIP is not supported for decisions." },
      "decision_from": { "type": "string", "format": "date", "description": "Required for search mode." },
      "decision_to": { "type": "string", "format": "date", "description": "Required for search mode." },
      "category": { "type": "array", "items": { "type": "string" }, "description": "e.g. Rezoning, Variance." },
      "decision_q": { "type": "string", "maxLength": 100 },
      "cursor": { "type": "string" },
      "size": { "type": "integer", "default": 20, "maximum": 100 }
    }
  },
  "annotations": { "readOnlyHint": true }
}
```

```json
{
  "name": "shovels_geo",
  "description": "Resolve free-text place names to Shovels geo_ids. Required first step before any permits/contractors/decisions search, since those endpoints reject free-text addresses.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string", "description": "Free-text address, city, county, jurisdiction, or state name." },
      "level": { "type": "string", "enum": ["address", "city", "county", "jurisdiction", "state"], "description": "Which resolver to use. Omit to try address first." }
    },
    "required": ["query"]
  },
  "annotations": { "readOnlyHint": true }
}
```

### B. Response shape — progressive disclosure in practice

Search mode (`shovels_permits`, no `id`):

```json
{
  "size": 3,
  "next_cursor": "tfZ.9525a96a93e0cdb7",
  "credits_remaining": 249701,
  "results": [
    {
      "id": "caf3b9d5ce317d53",
      "number": "RE2303928",
      "type": "electrical - 1 & 2 unit residential",
      "status": "active",
      "job_value_cents": 500000,
      "address": { "city": "OAKLAND", "state": "CA" },
      "contractor_id": "KOm4dMLIuT",
      "resource": "shovels://permits/caf3b9d5ce317d53"
    }
  ]
}
```

Fetch mode (`id` supplied) returns the full `PermitsRead` object as documented in Shovels' OpenAPI spec — all property_*, timing, and tag fields — since the agent explicitly asked for it.

### C. Known real constraints to design around

- `contractor_name` requires **3+ characters** (shorter strings can't use the trigram index).
- `permit_q` / `decision_q` are capped at 50 / 100 characters respectively.
- `total_count` is capped at 10,000 with an `{value, relation: "eq"|"gte"}` shape — don't treat it as an exact count above that.
- Decisions: **no ZIP-code filtering** — the upstream rezoning source doesn't carry ZIP data, only state/city/county/jurisdiction geo_ids.
- `job_value`, `fees`, `property_assess_market_value` are all in **cents** — surface this in tool descriptions so the agent doesn't misreport dollar amounts.
- Free trial is 250 requests total (not time-limited), flat rate regardless of result size — worth exposing remaining count prominently early on, since a wrapper that burns through someone's trial silently is a bad first impression.

### D. Build plan

1. Get a free API key (`app.shovels.ai/create-account`), confirm live responses against the schemas above.
2. Build the 4 tools as a thin FastMCP (Python) or `@modelcontextprotocol/sdk` (TS) server — each is a single HTTP call + shape transform.
3. Add internal cursor-session management and credit-header surfacing.
4. Test against Claude Desktop locally.
5. Package with a README that explicitly frames it as "the MCP server for the API you already ship — happy to talk about productizing this."

---

*Built against Shovels' public documentation as of July 2026. Field names, required parameters, and constraints above are pulled directly from their published OpenAPI spec — verify against `https://api.shovels.ai/spec/v2/openapi.production.yaml` before shipping, since it's a live spec that can change.*