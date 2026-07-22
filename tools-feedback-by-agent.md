# 🧪 Shovels MCP Tools — Full UX Test Report

> **Tester:** Claude Code (AI Agent simulating a user)
> **Date:** 2026-07-22
> **Scope:** All 4 MCP tools tested end-to-end
> **Format:** Each tool has its own section with test cases, findings, and recommendations.

---

## Tool 1: `shovels_geo` — Geo Resolution

### Test Cases Run

| # | Input | Level | Result |
|:-:|-------|-------|--------|
| 1 | `"TX"` | `state` | ✅ Resolved → `"TX"` / `"Texas"` |
| 2 | `"Austin, TX"` | auto | ⚠️ Resolved as **address-level** (street addresses), not city |
| 3 | `"90210"` | auto | ⚠️ Resolved as **address-level** (Beverly Hills addresses), not city |
| 4 | `"Taxas, AK"` | auto | ❌ Empty — no results, no suggestion |
| 5 | `"Texas, Alaska"` | auto | ❌ Empty — no results |
| 6 | `"Austin"` | `city` | ❌ Empty — city-level search has no data |
| 7 | `"Harris County"` | `county` | ❌ Empty |
| 8 | `"NY"` | `state` | ✅ `"NY"` / `"New York"` |
| 9 | `"New York City"` | auto | ⚠️ Address-level results only |
| 10 | `"!@#$%^&*()"` | auto | ❌ Empty — graceful silence |
| 11 | `""` (empty string) | auto | ⚠️ Returns first 5 states (AK, AL, AR, AZ, CA) |
| 12 | `"Houston"` | `city` | ❌ Empty |
| 13 | `"77001"` | `city` | ❌ Empty |
| 14 | `"AK"` | auto | ⚠️ Resolved as Alaska state |

### Key Findings

#### 🔴 Finding G1: City/County level resolution is dead
`level=city` and `level=county` always return empty, even for major cities like Austin and Houston. Users can't get a city geo_id directly — only state codes and street addresses work.

**Impact:** Users who want "permits in Austin" must use "TX" (state-level) and sift through all results, or know a specific address. This directly causes context bloat.

**Fix:** Either populate the city/county geo index, or expose a `shovels_geo` fallback that accepts city names and returns the best available geo_id.

#### 🔴 Finding G2: No fuzzy matching on typos
`"Taxas, AK"` → empty, `"Texas, Alaska"` → empty. No "Did you mean Texas (TX)?" or any suggestion.

**Fix:** Either add fuzzy matching in the MCP server, or wrap the geo tool to detect common patterns (state abbreviations, common typos) before delegating to the API.

#### 🟡 Finding G3: City/place queries fall through to address level with no feedback
`"Austin, TX"` returns street addresses like "1 Beecher Ln". The `level_matched: "address"` field is the only signal — easy to miss.

**Fix:** Surface a clear message like: *"No city-level match found. Showing street-level results for matching ZIP codes."*

#### 🟡 Finding G4: Empty string returns state list
`geo("")` returns first 5 states alphabetically — a footgun for unsanitized inputs.

**Fix:** Validate for empty/min-length input and return an error.

### Recommendations (Geo)

| Priority | Fix | Why |
|:--------:|-----|-----|
| 🔴 P0 | Fuzzy match + "did you mean?" for typos | Most common failure mode |
| 🔴 P0 | Populate city-level geo index or provide fallback | City queries are the #1 use case; current workaround causes 5x context bloat |
| 🟡 P1 | Surface `level_matched` more prominently | Users need to know if query resolved to state vs city vs address |
| 🟢 P2 | Block empty queries | Returning state list on empty input is a footgun |

---

## Tool 2: `shovels_permits` — Permit Search

### Test Cases Run

| # | Input | Result |
|:-:|-------|--------|
| 1 | `status=final` | ✅ 10 results |
| 2 | `status=active` | ✅ 10 results |
| 3 | `min_job_value=$100k` | ✅ 10 results (mixed residential/commercial) |
| 4 | `tags=new_construction` | ✅ 10 results |
| 5 | `geo_id=TX, 3mo` no filters | ⚠️ **162,771 chars / 5,596 lines** — context overflow |
| 6 | `ids=[...]` (from search) | ❌ **Empty** — fetch-by-ID doesn't work |
| 7 | `geo_id=INVALID` | ✅ Clean 422 with helpful message |
| 8 | No `geo_id` | ✅ Clean error message |
| 9 | `permit_tags=["commercial"]` | ❌ **Empty** — wrong filter for commercial queries |

### Key Findings

#### 🔴 Finding P1: No `property_type` filter → targeted queries are unusable
The #1 user need ("find commercial permits") requires `property_type=commercial` but no such parameter exists. Workaround: unfiltered search (5,596 lines) + manual filtering.

**Fix:** Add `property_type` as a query parameter (`commercial`, `residential`, `industrial`, `office`, `vacant_land`, `exempt`).

#### 🔴 Finding P2: `permit_tags` semantics are misleading
`tags: ["commercial"]` returns nothing. Tags are work-type labels (electrical, plumbing, roofing), not property classifications. Commercial permits have tags like `["plumbing"]`.

**Fix:** Document the tag taxonomy, or deprecate `permit_tags` in favor of `property_type` for classification queries.

#### 🟡 Finding P3: `total_count` is always null
```json
"total_count": null, "next_cursor": "5My.X..."
```
No idea if you're 10% or 90% through the data.

#### 🟡 Finding P4: Null-heavy responses (80%+ empty fields)
Each permit record has ~35 fields but only 5-8 are populated in search mode. 162k chars for 100 records when ~30k would suffice.

**Fix:** Add a compact search mode or strip null fields.

#### 🟡 Finding P5: Fetch-by-ID (`ids=`) returns empty
IDs from search results don't resolve via `GET /permits/{id}`. The search→drill-down UX pattern is broken.

### Recommendations (Permits)

| Priority | Fix | Why |
|:--------:|-----|-----|
| 🔴 P0 | Add `property_type` filter | Single highest-impact fix. Eliminates 90% of context waste. |
| 🔴 P0 | Fix fetch-by-ID | Drilling into details is a core UX pattern |
| 🟡 P1 | Compact search response (strip nulls) | 162k chars → ~30k for same data |
| 🟡 P1 | Surface total_count or estimate | Users can't tell if search is complete |
| 🟢 P2 | Document tag taxonomy | Users are guessing which tags to use |

---

## Tool 3: `shovels_contractors` — Contractor Search

### Test Cases Run

| # | Input | Result |
|:-:|-------|--------|
| 1 | `geo_id=TX, 2mo` no filters | ✅ 10 results with rich data (ratings, permit count, job value) |
| 2 | `contractor_name="ABC"` | ✅ 6 matching contractors |
| 3 | `classification_derived=["General"]` | ❌ Empty — no "General" classification in the data |
| 4 | `min_total_job_value=$5M` | ✅ 10 results (Brookfield $23.7B, etc.) |
| 5 | `contractor_name="AB"` (2 chars) | ✅ API validates min 3 chars |
| 6 | `ids=[...]` | ❌ **Empty** — same fetch issue as permits |
| 7 | `classification_derived=["electrical"]` | ✅ 5 results, works well |

### Key Findings

#### 🟡 Finding C1: `classification_derived` naming is confusing
Users won't guess this parameter — they'd try "classification" or "trade". The MCP tool description says "Filter by trade classification" but the param name is opaque.

**Fix:** Add a human-readable alias or list valid values in the description.

#### 🟡 Finding C2: Redundant fields
Duplicate fields like `phone` + `primary_phone`, `email` + `primary_email` add confusion.

**Fix:** Deduplicate — prefer the populated field over the null one.

#### 🟡 Finding C3: Fetch-by-ID broken (same as permits)
Returns empty for search-result IDs.

### Recommendations (Contractors)

| Priority | Fix | Why |
|:--------:|-----|-----|
| 🔴 P0 | Fix fetch-by-ID | Same core pattern issue as permits |
| 🟡 P1 | Add human-readable parameter aliases | `classification_derived` is not intuitive |
| 🟡 P1 | Deduplicate response fields | `phone`/`primary_phone`, `email`/`primary_email` confuse agents |
| 🟢 P2 | Add `min_rating` filter | Users often want vetted contractors |

---

## Tool 4: `shovels_decisions` — Zoning/Land-Use Decisions

### Test Cases Run

| # | Input | Result |
|:-:|-------|--------|
| 1 | `geo_id=TX, 2mo` no filters | ✅ **10 results, incredibly rich** — descriptions, `why_it_matters`, source URLs |
| 2 | `category=["Rezoning"]` | ❌ Empty — actual value is `"spot_rezoning"`, not `"Rezoning"` |
| 3 | `decision_q="commercial"` | ✅ 10 matching results |
| 4 | `decision_q` 200+ chars | ✅ Silently truncated to 100 (good handling) |
| 5 | `geo_id=77001` (ZIP) | ✅ Clean error: "ZIP not supported for decisions" |
| 6 | No `geo_id` | ✅ Clean error |
| 7 | `ids=[...]` | ❌ **Empty** — fetch-by-ID broken here too |
| 8 | `category=["Variance"]` | ❌ Empty |

### Key Findings

#### 🔴 Finding D1: `category` values don't match user expectations
The tool description says `"Rezoning"` but the API uses `"spot_rezoning"`, `"area_rezoning"`, `"zoning_code_modification"`. Users trying the obvious English category name get empty results.

**Fix:** Add a mapping layer or list valid values in the description.

#### 🟢 Finding D2: Data quality is exceptional
Decisions include `why_it_matters` summaries, `source_url`, `zoning_previous`/`zoning_new`, applicant/owner names. This is the **best data** of all 4 tools.

#### 🟡 Finding D3: No `category` taxonomy documented
The description says `(e.g. Rezoning, Variance)` but actual values include `spot_rezoning`, `zoning_code_modification`, `economic_development_incentives`, `land_use_planning`, `final_plat`, `project_amendments`, `city_properties`, `area_rezoning`.

**Fix:** Update the tool description to list actual values.

#### 🟡 Finding D4: `decision_q` silently truncates at 100 chars
The server does `decision_q[:100]` with no user feedback.

**Fix:** Return a warning when input exceeds the limit.

### Recommendations (Decisions)

| Priority | Fix | Why |
|:--------:|-----|-----|
| 🔴 P0 | Fix `category` value mismatch | Users trying "Rezoning" get empty results and think the tool is broken |
| 🟡 P1 | Document actual category taxonomy | Current description lists wrong example values |
| 🟡 P1 | Fix fetch-by-ID | Same as other tools |
| 🟢 P2 | Warn on `decision_q` truncation | Silent truncation confuses debugging |

---

## 🐛 Cross-Cutting Issues (All Tools)

### Issue X1: 🔴 Fetch-by-ID is broken across ALL 4 tools
Every tool accepts `ids` for full-record fetch mode, and every tool returns `"items": []`. The IDs returned by search mode don't resolve via `GET /{resource}/{id}`.

**Possible causes:**
1. Search result IDs differ from detail endpoint IDs
2. API auth differs between endpoints
3. MCP client serializes IDs incorrectly

**Fix:** Priority investigation — this breaks the fundamental search→drill-down pattern.

### Issue X2: 🟡 No rate-limit/cost feedback
Only `X-Credits-Request` is surfaced. With a 250-credit free trial, users need `X-Credits-Remaining`.

**Fix:** Surface credit headers in every response.

### Issue X3: 🟡 `total_count: null` everywhere
No tool reports total result count. Pagination is cursor-based with no cardinality estimate.

### Issue X4: 🟢 Empty query handling is inconsistent

| Tool | Empty geo_id behavior |
|------|:---------------------:|
| `shovels_geo` | Returns state list (bad) |
| `shovels_permits` | Clean error (good) |
| `shovels_contractors` | Clean error (good) |
| `shovels_decisions` | Clean error (good) |

---

## 📊 Priority Matrix

| Priority | Issue | Tool(s) | Impact |
|:--------:|-------|:-------:|--------|
| **🔴 P0** | No `property_type` filter | Permits | Can't query "commercial" → 5k-line responses |
| **🔴 P0** | Fetch-by-ID broken | All 4 | Search→detail pattern broken |
| **🔴 P0** | Geo fuzzy matching missing | Geo | Typos like "taxas, AK" hit dead ends |
| **🔴 P0** | Decision `category` values mismatch | Decisions | "Rezoning" filter returns empty |
| **🟡 P1** | City-level geo resolution missing | Geo | Forces state-level queries → bloat |
| **🟡 P1** | Compact search mode (strip nulls) | Permits | 80% null fields waste 162k chars |
| **🟡 P1** | `total_count` always null | All 4 | Blind pagination |
| **🟡 P1** | Credit header visibility | All 4 | 250-credit trial users blind to usage |
| **🟡 P1** | Tag/permit taxonomy undocumented | Permits | Users guess filters |
| **🟢 P2** | `decision_q` silent truncation | Decisions | Invisible data loss |
| **🟢 P2** | Empty geo query returns state list | Geo | Footgun for unsanitized inputs |
| **🟢 P2** | Parameter naming clarity | Contractors | `classification_derived` not intuitive |

---

## 🎯 Top 3 Fixes

If I could change only 3 things:

1. **Add `property_type` to permit search** — Turns "dump 5,596 lines and grep" into "return 36 matching records." Highest-leverage UX improvement.

2. **Fix fetch-by-ID mode** — Search→drill-down is fundamental to MCP. If passing IDs back returns nothing, users learn not to trust the tool.

3. **Add geo fuzzy matching** — Every agent/user will type a slightly wrong location. A "Did you mean X?" fallback turns failures into helpful responses.

---

*Generated from live testing of the Shovels MCP Server on 2026-07-22.*
