# Shovels MCP Server — How It Works

## Overview

The Shovels MCP Server is a lightweight proxy between AI agents and the [Shovels REST API](https://api.shovels.ai/v2). Instead of exposing 15+ raw endpoints, it consolidates everything into **4 MCP tools**.

```
Agent (Claude/Cursor/etc.) ──MCP──▶ Shovels MCP Server ──HTTP──▶ api.shovels.ai/v2
                                        │
                                        ├── shovels_geo        → addresses, cities, states
                                        ├── shovels_permits    → building permits
                                        ├── shovels_contractors→ contractors
                                        └── shovels_decisions  → zoning decisions
```

---

## Calling Sequence

Every query follows the same 3-step pattern:

```
Step 1:     shovels_geo("Austin, TX")
              │
              ▼  returns geo_id
Step 2:     shovels_permits(geo_id="TX", dates...)
              │
              ▼  returns search results (full records)
Step 3:     (optional) shovels_permits(ids=["..."])
              → fetches details by ID (may not work for all IDs)
```

### Why `shovels_geo` first?

The permits/contractors/decisions endpoints **require** a `geo_id` — they reject free-text addresses like "Austin, TX". `shovels_geo` converts place names to `geo_id` values.

---

## Tool Reference

### 1. `shovels_geo` — Resolve places to geo_ids

**Purpose:** Convert an address/city/state into a `geo_id` that other tools accept.

```
Required:  query (any place name)
Optional:  level  — "address" | "city" | "county" | "jurisdiction" | "state"
```

**With `level` specified:**
```json
{"query": "TX", "level": "state"}
→ {"geo_id": "TX", "name": "Texas"}

{"query": "Austin, TX", "level": "jurisdiction"}
→ {"geo_id": "q8fdm_HmVcc", "name": "Austin, TX"}
```

**Without `level`** (auto fallback):
The tool tries address → city → county → jurisdiction → state and returns the first match.

**Known limitations:**
| Level | Works? | Notes |
|---|---|---|
| `state` | ✅ | Use 2-letter codes ("TX", "CA"), not full names |
| `jurisdiction` | ✅ | Works for most cities |
| `address` | ✅ | Full street addresses |
| `city` | ❌ | Shovels API returns empty |
| `county` | ❌ | Shovels API returns empty |

### 2. `shovels_permits` — Search building permits

**Purpose:** Find building permits by location and date range.

```
Required:  geo_id + permit_from + permit_to
Optional:  permit_status, permit_tags, permit_min_job_value,
           contractor_classification_derived, cursor, size (max 100)
```

**Search mode** (returns full records with all fields):
```json
{"geo_id": "TX", "permit_from": "2026-01-01", "permit_to": "2026-06-30", "size": 5}
```

**With filters:**
```json
{
  "geo_id": "TX",
  "permit_from": "2026-01-01",
  "permit_to": "2026-06-30",
  "permit_status": ["final"],
  "size": 3
}
```

**Error messages are descriptive:**
- Missing `geo_id` → `"geo_id is required. Use shovels_geo to resolve a location first."`
- Invalid `geo_id` → Shows the exact API error with accepted formats
- Missing dates → `"permit_from is required (YYYY-MM-DD)."`

**💰 All monetary values are in cents** (job_value, fees, property_assess_market_value).

### 3. `shovels_contractors` — Search contractors

**Purpose:** Find contractors active in a geography.

```
Required:  geo_id + permit_from + permit_to
Optional:  contractor_name (min 3 chars), contractor_classification_derived,
           contractor_min_total_job_value, cursor, size (max 100)
```

```json
{"geo_id": "TX", "permit_from": "2026-01-01", "permit_to": "2026-06-30", "contractor_name": "BEST", "size": 5}
```

The search results already contain detailed contractor info (phone, email, address, permit_count, total_job_value, etc.).

### 4. `shovels_decisions` — Search zoning/land-use decisions

**Purpose:** Find rezoning, variance, and other land-use decisions.

```
Required:  geo_id + decision_from + decision_to
Optional:  category, decision_q (max 100 chars), cursor, size (max 100)
```

**⚠️ ZIP codes NOT supported** for decisions — use state or jurisdiction geo_id.

```json
{"geo_id": "TX", "decision_from": "2026-01-01", "decision_to": "2026-06-30", "size": 3}
```

---

## Response Format

All tools return JSON with this structure:

**Success:**
```json
{
  "items": [...],           // Array of records
  "size": 2,                // Number of records returned
  "next_cursor": null,      // Pagination cursor (null = no more pages)
  "X-Credits-Remaining": "249"  // Shovels API credits left
}
```

**Error:**
```json
{
  "error": "Clear description of what went wrong",
  "note": "Helpful hint about how to fix it"
}
```

---

## What Each Tool Returns

### Permits (full records)
| Field | Description |
|---|---|
| `id` | Unique permit ID |
| `number` | Permit number |
| `type` / `subtype` | Permit classification |
| `status` | final, in_review, inactive, active |
| `job_value` | **Cents** |
| `fees` | **Cents** |
| `description` | Work description |
| `file_date` / `issue_date` / `final_date` | Timeline |
| `contractor_id` | Linked contractor |
| `tags` | Labels (e.g. "roofing", "electrical") |
| `address` | Street, city, state, zip, lat/lng |
| `geo_ids` | Address, city, jurisdiction geo_ids |
| `property_*` | Type, lot size, year built, market value |

### Contractors (full records)
| Field | Description |
|---|---|
| `id` | Unique contractor ID |
| `name` / `business_name` | Company name |
| `primary_phone` / `primary_email` | Contact info |
| `permit_count` | Number of permits |
| `avg_job_value` / `total_job_value` | **Cents** |
| `status_tally` / `tag_tally` | Breakdown of permit activity |
| `address` | Street, city, state |

### Decisions (full records)
| Field | Description |
|---|---|
| `id` | Unique decision ID |
| `title` | Decision title |
| `description` | Full description |
| `decision_date` | Date of decision |
| `category` / `subcategory` | Classification |
| `city` / `state` | Location |
| `source_url` | Link to original document |

---

## Error Handling

### Common errors and their causes

| Error | Cause | Fix |
|---|---|---|
| `geo_id is required` | Called search without geo_id | Run `shovels_geo` first |
| `permit_from is required` | Missing date parameter | Add `YYYY-MM-DD` date |
| `Invalid geolocation ID 'X'` | Wrong geo_id format | Use 2-letter state code, ZIP, or Shovels geo_id |
| `Shovels API error 401` | API key missing/invalid | Check `SHOVELS_API_KEY` in `.env` |
| `Not Found` (fetch by ID) | Individual GET endpoint unavailable | Use search with geo_id + dates instead |
| `Rate limited (429)` | Out of credits | Check remaining credits in response |

### Fetch by ID limitation

The Shovels API does **not** expose individual `GET /{resource}/{id}` endpoints for most resource types. The search endpoints already return complete records. The `ids` parameter will attempt fetch-by-ID but may return a "Not Found" message with a suggestion to search instead.

---

## Credits & Rate Limits

- Free trial: **250 requests** (flat, any size)
- Every response includes `X-Credits-Remaining` so the agent can track usage
- 429 errors are handled cleanly with a descriptive message
