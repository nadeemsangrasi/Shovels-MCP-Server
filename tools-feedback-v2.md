# 🧪 Shovels MCP Tools — UX Test Report v2

> **Tester:** Claude Code (AI Agent simulating a user)
> **Test Date:** 2026-07-22
> **Scope:** Re-test of all 4 MCP tools after v1 feedback was addressed
> **Status Legend:** ✅ Fixed | 🟡 Partial | 🔴 Still Open | 🆕 New Finding

---

## v1 → v2 Change Log

| # | Issue | Status | Notes |
|:-:|-------|:------:|-------|
| P1 | No `property_type` filter on permits | ✅ Fixed | Added, returns 100 commercial permits in 1 call |
| P2 | No fuzzy geo matching | ✅ Fixed | "Taxas" → "TX" with `_note` |
| P3 | Null-heavy responses | ✅ Fixed | `_strip_nulls` compacts records 24% |
| P4 | Decision category values mismatch | ✅ Fixed | Docs list actual API values |
| P5 | `decision_q` silent truncation | ✅ Fixed | Returns `_warning` when truncated |
| P6 | Empty geo query returns state list | ✅ Fixed | Returns clean error |
| P7 | Geo address fallback silent | ✅ Fixed | `_note` suggests broader level |
| P8 | Tag taxonomy undocumented | ✅ Fixed | Docs updated with values |
| X1 | Fetch-by-ID broken (all tools) | 🔴 Open | Still returns empty |
| X2 | `total_count` always null | 🔴 Open | No cardinality info |
| X3 | Credit headers not surfaced | 🔴 Open | Only `X-Credits-Request` returned |

---

## Tool 1: `shovels_geo` — Geo Resolution

### v1 Findings Re-test

| # | Input | v1 Result | v2 Result |
|:-:|-------|-----------|-----------|
| 1 | `"Taxas"` | ❌ Empty | ✅ **Auto-corrected** → `"TX"` with `_note` |
| 2 | `""` (empty) | ⚠️ Returned 5 states | ✅ **Clean error**: "query is required" |
| 3 | `"Austin, TX"` | ⚠️ Silent address fallback | ✅ `_note` suggests using `level='state'` |
| 4 | `"california"` | ⚠️ Address-level garbage | ⚠️ Still address-level (`"California, MD"`) — `_note` present but wrong result |
| 5 | `"NY"` | ✅ State level | ✅ Same — no regression |
| 6 | `"!@#$%^&*()"` | ❌ Empty | ❌ Still empty (graceful, acceptable) |

### Remaining Issues

#### 🟡 Geo G5: State name → address level fallback is still wrong for common state names
`"california"` resolves to address-level results for the town "California, MD" and "California, KY" instead of recognizing it as California (state CA). The fuzzy matching only kicks in for `level="state"` or short queries.

**Fix:** Extend `_guess_state_code` to run even for non-short queries. If a full state name matches, auto-resolve to the state code.

---

## Tool 2: `shovels_permits` — Permit Search

### v1 Findings Re-test

| # | Scenario | v1 Result | v2 Result |
|:-:|----------|-----------|-----------|
| 1 | `property_type=commercial` | ❌ No param existed | ✅ **Works** — returns commercial permits directly |
| 2 | `property_type=commercial` (100 items) | N/A | ✅ Returns 100 commercial records in 1 page |
| 3 | Unfiltered search (3mo) | ⚠️ 162,771 chars / 5,596 lines | ✅ **Compact:** 24% smaller per-record (nulls stripped) |
| 4 | `permit_tags=["commercial"]` | ❌ 0 results | ❌ Still 0 — tags aren't property types. Doc now clarifies this. |
| 5 | `ids=[...]` (fetch-by-ID) | ❌ Empty | ❌ **Still empty** — not fixed |
| 6 | `geo_id=INVALID` | ✅ Clean 422 | ✅ Same |
| 7 | No `geo_id` | ✅ Clean error | ✅ Same |

### Sample — Commercial + New Construction
```json
{
  "number": "2026-88035",
  "description": "Htx autonation llc - small office of 435 square ft for car sales",
  "property_type": "commercial",
  "type": "Development",
  "status": "in_review",
  "job_value": 0,
  "tags": ["new_construction"]
}
```
Now only 13 fields, down from ~35. ✅

---

## Tool 3: `shovels_contractors` — Contractor Search

### v1 Findings Re-test

| # | Scenario | v1 Result | v2 Result |
|:-:|----------|-----------|-----------|
| 1 | `classification_derived=["electrical"]` | ✅ Worked | ✅ Same, compacted |
| 2 | `classification_derived=["General"]` | ❌ Empty | ❌ Still empty — "General" isn't a valid value |
| 3 | `contractor_name="AB"` (2 chars) | ✅ API validation | ✅ Same |
| 4 | `ids=[...]` | ❌ Empty | ❌ **Still empty** — not fixed |
| 5 | Duplicate fields (`phone`/`primary_phone`) | 🟡 Confusing | 🟡 Still present but less visible due to `_strip_nulls` |

---

## Tool 4: `shovels_decisions` — Zoning/Land-Use Decisions

### v1 Findings Re-test

| # | Scenario | v1 Result | v2 Result |
|:-:|----------|-----------|-----------|
| 1 | `category=["spot_rezoning"]` | ⚠️ Wrong value used ("Rezoning") | ✅ **Works** — docs now list API values |
| 2 | `decision_q` 265 chars | ❌ Silent truncation | ✅ `_warning: "truncated from 265 to 100"` |
| 3 | `decision_q="commercial"` | ✅ Rich results | ✅ Same |
| 4 | `ids=[...]` | ❌ Empty | ❌ **Still empty** — not fixed |
| 5 | `geo_id=77001` (ZIP) | ✅ Clean error | ✅ Same |

---

## 🐛 Still Open: Cross-Cutting Issues

### Issue X1 (🔴 P0): Fetch-by-ID broken on ALL 4 tools
Every tool returns `"items": []` when passed IDs from search results.

**Impact:** The search→drill-down UX is non-functional. Users/agents can find permits but can't get full details.

**Example:**
```
shovels_permits(ids=["a4a58e10def4669c"])  →  {items: [], ...}
shovels_contractors(ids=["00aPTOiM0z"])  →  {items: [], ...}
shovels_decisions(ids=["02539c85-1700-4040-ab60-bc72255caa69"])  →  {items: [], ...}
```

### Issue X2 (🟡 P1): `total_count` always null
No pagination cardinality across all tools.

### Issue X3 (🟡 P1): Credit headers not surfaced
`X-Credits-Remaining` is not in any response — critical for 250-credit free trial users.

---

## 📊 v2 Scorecard

| Area | v1 State | v2 State | Grade |
|------|:--------:|:--------:|:-----:|
| Geo fuzzy matching | ❌ Broken | ✅ Auto-corrects typos | **A** |
| Geo empty query | ❌ Footgun | ✅ Clean error | **A** |
| `property_type` filter | ❌ Missing | ✅ Added | **A+** |
| Response compactness | ❌ Bloated | ✅ 24% smaller | **B+** |
| Decision categories | ❌ Wrong docs/values | ✅ Docs fixed | **A** |
| `decision_q` truncation | ❌ Silent | ✅ Warns user | **A** |
| Tag taxonomy docs | ❌ Missing | ✅ Documented | **A** |
| Fetch-by-ID | ❌ Broken | ❌ Still broken | **F** |
| `total_count` | ❌ Missing | ❌ Missing | **C** |
| Credit header visibility | ❌ Missing | ❌ Missing | **C** |

**Overall: 7/10 issues fixed.** The `property_type` filter is the single biggest improvement — it makes the tool actually usable for targeted queries.

---

## 🎯 Priority for v3

1. **Fix fetch-by-ID** — The last critical UX blocker
2. **Surface `X-Credits-Remaining`** — Essential for free trial users
3. **Better state name recognition** — `"california"` should resolve to `"CA"`

---

*Re-test performed 2026-07-22 against the updated Shovels MCP Server.*
