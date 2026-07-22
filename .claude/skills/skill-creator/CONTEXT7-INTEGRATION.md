# Context7 MCP Integration Guide

This document explains how the skill-creator integrates with Context7 MCP for fetching official documentation.

## What is Context7?

Context7 is a Model Context Protocol (MCP) server that allows Claude to fetch official documentation for various technologies, frameworks, libraries, and APIs directly from their sources.

## Why Use Context7 with Skills?

When creating skills for specific technologies, Context7 provides:

1. **Accuracy**: Official documentation ensures correct information
2. **Currency**: Always get up-to-date best practices
3. **Completeness**: Comprehensive reference materials
4. **Offline Access**: Store docs locally with the skill
5. **Best Practices**: Follow framework-recommended patterns

## When to Use Context7

### Good Use Cases ✓

- **Frameworks**: React, Vue, Django, FastAPI, Express, Rails, etc.
- **Libraries**: pytest, pandas, requests, numpy, lodash, etc.
- **APIs**: GitHub, Stripe, AWS, Google Cloud, Twilio, etc.
- **Languages**: Python patterns, JavaScript features, Go idioms, etc.
- **Tools**: Docker, Kubernetes, Terraform, Jenkins, etc.

### When NOT to Use ✗

- Generic workflows (git commits, file organization)
- Internal company processes
- Custom/proprietary tools
- Simple utility tasks
- Language-agnostic patterns

## How to Use Context7 in Skill Creation

### Step 1: Identify Documentation Needs

Before creating the skill, list what official docs you need:

```markdown
Example: Creating "fastapi-developer" skill

Documentation needed:
- FastAPI official guide
- Pydantic models reference
- SQLAlchemy async patterns
- Uvicorn server configuration
```

### Step 2: Fetch Documentation

Ask Claude to fetch docs via Context7:

```
"Use Context7 to fetch FastAPI official documentation"
"Get Pydantic models documentation via Context7"
"Fetch SQLAlchemy async patterns using Context7"
```

Claude will retrieve and save the documentation to your skill's `references/` directory.

### Step 3: Organize Documentation

Create a clear structure:

```
skill-name/references/
├── official-docs/              # From Context7
│   ├── fastapi-guide.md
│   ├── pydantic-models.md
│   └── sqlalchemy-async.md
├── summaries/                  # Your condensed versions
│   ├── quick-start.md
│   └── common-patterns.md
└── examples/                   # Your practical examples
    ├── basic-usage.md
    └── advanced-patterns.md
```

### Step 4: Reference in SKILL.md

Make documentation easily accessible:

```markdown
## Prerequisites

### Official Documentation
- FastAPI Guide: `references/official-docs/fastapi-guide.md`
- Pydantic Models: `references/official-docs/pydantic-models.md`
- SQLAlchemy Async: `references/official-docs/sqlalchemy-async.md`

### Quick References
- Quick Start: `references/summaries/quick-start.md`
- Common Patterns: `references/summaries/common-patterns.md`

## Instructions

### Step 1: Project Setup

Follow the official FastAPI setup guide: `references/official-docs/fastapi-guide.md`

Key steps from official documentation:
1. Install FastAPI and Uvicorn
2. Create main application file
3. Define your first endpoint

Example from official docs:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

See complete guide for advanced configuration.
```

## Complete Example: FastAPI Skill

### 1. Create Skill Structure

```bash
python3 scripts/create-skill-structure.py \
  --name "fastapi-developer" \
  --location personal
```

### 2. Fetch Official Documentation

```
User: "Use Context7 to fetch FastAPI official documentation"
```

Claude fetches and saves to:
- `references/official-docs/fastapi-guide.md`

```
User: "Use Context7 to fetch Pydantic models documentation"
```

Saves to:
- `references/official-docs/pydantic-models.md`

```
User: "Use Context7 to fetch SQLAlchemy async patterns"
```

Saves to:
- `references/official-docs/sqlalchemy-async.md`

### 3. Create Summaries

Create quick reference guides based on fetched docs:

**`references/summaries/quick-start.md`:**
```markdown
# FastAPI Quick Start

Based on: `../official-docs/fastapi-guide.md`

## Installation
```bash
pip install fastapi uvicorn[standard]
```

## Minimal Application
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## Running
```bash
uvicorn main:app --reload
```

Visit: http://localhost:8000

For complete documentation, see the official guide.
```

### 4. Generate and Populate SKILL.md

```bash
python3 scripts/generate-skill-template.py \
  --name "fastapi-developer" \
  --description "Build FastAPI applications following official best practices. Use when creating REST APIs, async endpoints, or FastAPI projects." \
  --allowed-tools "Bash, Read, Write" \
  --tags "fastapi, python, api, backend" \
  --output ~/.claude/skills/fastapi-developer/SKILL.md
```

Then edit SKILL.md to reference the documentation:

```markdown
## Instructions

### Step 1: Project Setup

Refer to official setup: `references/official-docs/fastapi-guide.md`
Quick reference: `references/summaries/quick-start.md`

1. Install dependencies
2. Create project structure
3. Set up database (see `references/official-docs/sqlalchemy-async.md`)

### Step 2: Define Models

Use Pydantic models: `references/official-docs/pydantic-models.md`

Example from official documentation:
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    price: float = Field(gt=0, description="Price must be positive")
    tax: float | None = None
```
```

## Best Practices

### 1. Fetch Early

Get documentation BEFORE writing instructions:

```
Workflow:
1. Create skill structure
2. Fetch Context7 documentation ← Early
3. Review fetched docs
4. Write SKILL.md based on official patterns
5. Create summaries for quick access
```

### 2. Keep Documentation Updated

Add version notes:

```markdown
## References

### Official Documentation
- FastAPI Guide: `references/official-docs/fastapi-guide.md`
  - Fetched: 2026-01-01
  - Version: FastAPI 0.104.0
  - Note: Re-fetch for major version updates
```

### 3. Create Useful Summaries

Don't just store raw docs—make them actionable:

- **Quick Start**: Essential setup steps
- **Common Patterns**: Frequently used code patterns
- **Troubleshooting**: Common issues and solutions
- **Cookbook**: Practical examples

### 4. Organize by Purpose

```
references/
├── official-docs/          # Complete references (when needed)
│   ├── framework-guide.md
│   └── api-reference.md
├── summaries/             # Quick lookups
│   ├── quick-start.md
│   └── cheat-sheet.md
└── examples/              # Practical applications
    ├── basic-app.md
    └── advanced-patterns.md
```

## Common Patterns

### Pattern 1: Framework Skill

```
Skill: react-testing
Context7: React Testing Library, Jest, React hooks testing
Structure:
- references/official-docs/react-testing-library.md
- references/official-docs/jest-config.md
- references/summaries/testing-patterns.md
```

### Pattern 2: Library Integration

```
Skill: pandas-analysis
Context7: pandas documentation, numpy reference
Structure:
- references/official-docs/pandas-guide.md
- references/official-docs/numpy-reference.md
- references/summaries/data-manipulation.md
```

### Pattern 3: API Integration

```
Skill: github-automation
Context7: GitHub REST API, GitHub Actions
Structure:
- references/official-docs/github-rest-api.md
- references/official-docs/github-actions.md
- references/examples/automation-workflows.md
```

## Maintenance

### When to Re-fetch

Re-fetch Context7 documentation when:

- Major framework version updates
- Significant API changes announced
- Deprecation warnings in your skill
- Users report outdated information
- Quarterly documentation review

### Version Tracking

Track documentation versions:

```markdown
## Documentation Version History

### v2.0.0 (2026-03-01)
- Updated FastAPI docs to v0.110.0
- Added new async patterns
- Refreshed Pydantic models for v2.0

### v1.0.0 (2026-01-01)
- Initial documentation fetch
- FastAPI v0.104.0
- Pydantic v1.10.0
```

## Benefits Summary

**For Skill Creators:**
- ✓ Saves research time
- ✓ Ensures accuracy
- ✓ Provides comprehensive references
- ✓ Follows official best practices
- ✓ Makes skills maintainable

**For Skill Users:**
- ✓ Trustworthy information
- ✓ Official patterns
- ✓ Up-to-date practices
- ✓ Complete references
- ✓ Offline documentation

## FAQ

### Q: Can I use Context7 for any technology?

A: Context7 supports most major frameworks, libraries, and APIs with official documentation. If documentation isn't available via Context7, you can still manually add references.

### Q: How often should I update fetched documentation?

A: Review quarterly or when major versions release. Re-fetch if APIs change significantly.

### Q: What if Context7 isn't available?

A: Skills work fine without Context7. You can manually add documentation or reference external URLs. Context7 just makes it easier and provides offline access.

### Q: Should I store all documentation in the skill?

A: Store essential guides and API references. For very large documentation sets, store summaries and key sections, with links to complete docs.

### Q: Can I edit Context7-fetched documentation?

A: Keep official docs intact. Create separate summary files for your edits and condensed versions.

## Resources

- Context7 MCP Documentation: [link if available]
- MCP Protocol Spec: https://modelcontextprotocol.io
- Claude Code Skills Guide: https://docs.claude.com/skills

---

**Integration Added**: 2026-01-01
**Version**: 1.0.0
