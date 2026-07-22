# Skill Integration with Context7

## Overview

Integrate Context7 documentation into existing skills to provide up-to-date, authoritative information.

## Integration Patterns

### Pattern 1: Link to Context7

Add Context7 links to existing skills:

```markdown
**External Resources:**
- [Official Documentation](https://docs.library.com)
- [Context7 Documentation](context7:/library-id)
```

### Pattern 2: Fetch on Demand

Use Context7 to enhance skills:

```markdown
For the latest examples, use:
mcp__context7__query-docs("/library-id", "specific feature")
```

### Pattern 3: Create Sub-References

Create references for specific integrations:

```
.claude/skills/skill-name/
└── references/
    └── library-integration.md  # Created from Context7
```

## Integration Examples

### With better-auth-nextjs

```
1. Resolve library: mcp__context7__resolve-library-id("better-auth", "jwt plugin")
2. Query: "better-auth JWT configuration examples"
3. Create: .claude/skills/better-auth-nextjs/references/jwt.md
```

### With scaffolding-fastapi

```
1. Resolve library: mcp__context7__resolve-library-id("fastapi", "database integration")
2. Query: "FastAPI SQLAlchemy async database session"
3. Create: .claude/skills/scaffolding-fastapi/references/async-db.md
```

### With docker-containerization

```
1. Resolve library: mcp__context7__resolve-library-id("docker", "multi-stage build")
2. Query: "Docker multi-stage build production optimization"
3. Create: .claude/skills/docker-containerization/references/multi-stage.md
```

## Updating Skills

When integrating Context7:

1. **Identify gaps** - What needs current documentation?
2. **Resolve libraries** - Get correct Context7 IDs
3. **Fetch docs** - Query specific features
4. **Create references** - Save useful patterns
5. **Update skills** - Add links and references

## Cross-Reference Structure

```markdown
# Library Integration Reference

## Source
- Context7 ID: /library-id
- Query: "your query"

## Integration Points
- Used in: skill-name
- Reference: .claude/skills/skill-name/references/feature.md

## Code Example
```typescript
// From Context7
code here
```

## Integration Notes
- How to use in skill
- Dependencies
- Configuration
```

## Benefits

1. **Always current** - Context7 provides latest docs
2. **Authoritative** - Official documentation sources
3. **Comprehensive** - Large code snippet collection
4. **Versioned** - Can specify versions
5. **Searchable** - Find specific patterns
