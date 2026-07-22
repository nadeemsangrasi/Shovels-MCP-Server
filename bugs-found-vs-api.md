# Bug Report: Issues Found in Shovels MCP Server vs API

## Tested directly against `api.shovels.ai/v2` with live API key

---

### Bug 1: Geo resolution broken for `city` and `county` levels

**Our bug.** The `resolve_geo` method appends "s" to every level name:

```python
f"{lvl}s/search"
# city → "citys/search" ❌ (should be "cities/search")
# county → "countys/search" ❌ (should be "counties/search")
```

The API endpoint uses irregular plurals. Direct curl test confirms:

```
GET /cities/search?q=Austin,%20TX          → 200 ✅  (returns geo_id: a4xysKbZwqg)
GET /citys/search?q=Austin,%20TX           → 404 ❌
GET /jurisdictions/search?q=Austin         → 200 ✅  (returns geo_id: q8fdm_HmVcc)
```

**Fix applied:** Added correct pluralization mapping.

---

### Bug 2: Permit and Contractor fetch by ID returns 404

**Not our bug — it's a Shovels API issue.** Confirmed with direct API calls:

```
GET /permits/3f88270a8fa68443              → 404 ❌
  (same ID found in search results ✅)

GET /contractors/HjeJljeoDZ                → 404 ❌
```

The IDs returned by `GET /permits/search` and `GET /contractors/search` are **not accepted by** `GET /permits/{id}` and `GET /contractors/{id}`. This is an API data integrity issue — the search and detail endpoints use incompatible IDs.

---

### Bug 3: Tags endpoint returns 404

**Not our bug — endpoint doesn't exist in this API version.** Tested every variation:

```
GET /tags             → 404 ❌
GET /permit_tags      → 404 ❌
GET /tags/list        → 404 ❌
GET /meta/tags        → 404 ❌
```

---

### Summary for Shovels Team

| Issue                           | Root Cause                                     | Severity             |
| ------------------------------- | ---------------------------------------------- | -------------------- |
| City/county geo fails           | Our code: wrong pluralization in endpoint path | **Fixed**            |
| Permit/contractor get-by-ID 404 | API: search IDs ≠ detail endpoint IDs          | **Upstream bug**     |
| Tags endpoint 404               | API: `/tags` endpoint doesn't exist            | **Missing endpoint** |

# 1. Build the image

cd backend
docker build -t shovels-mcp .

# 2. Run the container (no API key env var needed)

docker run -p 7860:7860 shovels-mcp
