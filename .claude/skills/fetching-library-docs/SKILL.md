---
name: fetching-library-docs
description: Use Context7 MCP to fetch up-to-date documentation and code examples for any library. Use when you need official documentation, API references, code snippets, or examples for libraries like FastAPI, Next.js, React, Docker, or any library available on Context7.
version: 1.0.0
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__context7__resolve-library-id, mcp__context7__query-docs
author: Claude Code
tags: [context7, documentation, api-reference, code-examples, library-docs, fetch-docs, mcp, research, learning, integration]
---

# Fetching Library Docs with Context7 MCP

Use Context7 MCP to fetch up-to-date official documentation and code examples for any library. Get accurate, version-specific information without relying on potentially outdated internal knowledge.

## Overview

Context7 MCP provides access to official library documentation from sources like official websites, GitHub repositories, and documentation platforms. This skill helps you:

- Find the right library ID for any library
- Fetch official documentation and examples
- Get version-specific information
- Create reference materials for your projects

## When to Use This Skill

**Activate when:**
- You need documentation for a specific library
- You want code examples for an API
- You're integrating a new library
- You need to verify API signatures or options
- You're learning how to use a library feature
- You need troubleshooting guidance

**Trigger keywords:** "context7", "fetch docs", "library documentation", "api reference", "code examples", "official docs", "get documentation", "learn library", "library docs"

**NOT for:**
- General web search (use web search skill)
- Non-programming documentation
- Outdated or unofficial sources

## Prerequisites

**Required:**
- Context7 MCP server configured and running
- Library name or package name to search

**Recommended:**
- Understanding of what you want to achieve with the library
- Access to a code editor for implementing solutions

## Instructions

### Phase 1: Find the Library

#### Step 1: Resolve Library ID

**Use when:** You know the library name but need the Context7 ID.

**Example queries:**
```
Library: "fastapi" → /fastapi/fastapi
Library: "nextjs" → /vercel/next.js
Library: "react" → /facebook/react
Library: "docker" → /docker/docs
```

**Pattern:**
```
Use mcp__context7__resolve-library-id with:
- libraryName: "package-name"
- query: "what you want to accomplish"
```

**See:** `references/resolving-libraries.md`

#### Step 2: Verify Library Selection

**Check the results:**
- Library ID format: `/org/project` or `/org/project/version`
- Benchmark score (higher = better quality)
- Code snippet count (more = more examples)
- Source reputation (High/Medium/Low)

**If multiple matches:**
- Choose the official documentation (highest benchmark)
- Check version availability
- Consider snippet count for examples

### Phase 2: Fetch Documentation

#### Step 3: Query Documentation

**Use when:** You have the library ID and need specific information.

**Pattern:**
```
Use mcp__context7__query-docs with:
- libraryId: "/org/project" (from Step 1)
- query: "specific question about the library"
```

**Good queries:**
- "How to create a FastAPI endpoint with query parameters"
- "React useEffect cleanup function examples"
- "Dockerfile multi-stage build best practices"
- "Next.js 14 app router data fetching"

**Avoid:**
- Too vague: "React docs"
- Too broad: "Everything about Docker"
- Already known: Things you already understand

**See:** `references/querying-docs.md`

#### Step 4: Process Results

**Review the output:**
- Code snippets are most useful
- Explanations provide context
- Links point to full documentation

**Extract key information:**
```markdown
## Library: LibraryName

### Key Concepts
- Concept 1: Description
- Concept 2: Description

### Code Example
```language
// Code from documentation
```

### Common Patterns
- Pattern 1: How to use
- Pattern 2: How to use
```

### Phase 3: Apply to Codebase

#### Step 5: Create Reference Files

**Create project-specific references:**
```bash
mkdir -p .claude/skills/library-name/references
```

**Document patterns you use:**
- `.claude/skills/library-name/references/usage.md`
- `.claude/skills/library-name/references/examples.md`
- `.claude/skills/library-name/references/troubleshooting.md`

**See:** `references/creating-references.md`

#### Step 6: Implement the Solution

**Follow the patterns from docs:**
```typescript
// Use the exact pattern from documentation
import { library } from 'library';

const result = await library.function({
  // Use documented options
  option: value,
});
```

**Test with examples from docs:**
```bash
# Run the example code
npm test  # or appropriate test command
```

### Phase 4: Integrate with Skills

#### Step 7: Cross-Reference Skills

**Link to related skills:**
- `better-auth-nextjs` references Next.js docs
- `scaffolding-fastapi` references FastAPI docs
- `docker-containerization` references Docker docs

**Update skill references:**
```markdown
**External Resources:**
- [Official Documentation](context7-link)
```

**See:** `references/skill-integration.md`

## Common Patterns

### Pattern 1: New Library Integration
**Quick:** Resolve ID → Query docs → Create reference → Implement

**See:** `references/examples.md#new-library`

### Pattern 2: Feature Implementation
**Quick:** Query specific feature → Get code examples → Apply pattern

**See:** `references/examples.md#feature`

### Pattern 3: Troubleshooting
**Quick:** Query error → Get solution from docs → Apply fix

**See:** `references/examples.md#troubleshooting`

### Pattern 4: Version Migration
**Quick:** Query version-specific docs → Compare patterns → Update code

**See:** `references/examples.md#migration`

## Quick Reference

### MCP Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `mcp__context7__resolve-library-id` | Find library ID | Resolve "fastapi" → `/fastapi/fastapi` |
| `mcp__context7__query-docs` | Get documentation | Query "FastAPI CRUD endpoints" |

### Query Strategies

**Specific questions:**
- "How to validate form input in React"
- "FastAPI dependency injection examples"
- "Docker multi-stage build Python"

**Comparative queries:**
- "Express vs FastAPI routing"
- "React useState vs useReducer"

**Troubleshooting queries:**
- "Next.js dynamic routes 404"
- "React useEffect strict mode double mount"

## Error Handling

| Issue | Cause | Solution |
|-------|-------|----------|
| No library found | Typo in name | Verify spelling, try alternative names |
| Wrong library selected | Generic name | Use more specific query |
| Empty results | Too specific query | Broaden query terms |
| Outdated info | Wrong version | Specify version in libraryId |

**See:** `references/troubleshooting.md`

## Best Practices

1. **Always verify** - Cross-check multiple sources
2. **Be specific** - Detailed queries get better results
3. **Version matters** - Use version-specific IDs when available
4. **Extract patterns** - Create reusable reference files
5. **Document sources** - Link back to Context7 docs
6. **Test examples** - Verify code from docs works
7. **Stay current** - Re-query for updates

## Validation Checklist

**Library Finding:**
- [ ] Library ID resolved correctly
- [ ] Correct library selected (check benchmark)
- [ ] Version verified if needed

**Documentation:**
- [ ] Query returned relevant results
- [ ] Code snippets extracted
- [ ] Key concepts understood

**Application:**
- [ ] Code implemented from examples
- [ ] Tests pass
- [ ] Reference file created

## Quick Commands

**Find a library:**
```
mcp__context7__resolve-library-id with:
- libraryName: "package-name"
- query: "what you want to do"
```

**Get specific documentation:**
```
mcp__context7__query-docs with:
- libraryId: "/org/project"
- query: "specific question"
```

**Example workflow:**
```bash
# 1. Find library
mcp__context7__resolve-library-id("react", "hooks")

# 2. Get documentation
mcp__context7__query-docs("/facebook/react", "useEffect examples")

# 3. Create reference
# Write to .claude/skills/react/references/useEffect.md
```

## References

**Local Documentation:**
- Resolving libraries: `references/resolving-libraries.md`
- Querying docs: `references/querying-docs.md`
- Creating references: `references/creating-references.md`
- Skill integration: `references/skill-integration.md`
- Examples: `references/examples.md`
- Troubleshooting: `references/troubleshooting.md`

**External Resources:**
- [Context7 MCP Documentation](https://context7.com)
- [MCP Protocol](https://modelcontextprotocol.io)

## Tips for Success

1. **Start with the library name** - Resolve ID first
2. **Be specific in queries** - "How to X in library Y"
3. **Check benchmark scores** - Higher is better
4. **Extract and save** - Create reference files
5. **Test code examples** - Verify they work
6. **Link sources** - Document where info came from
7. **Re-query when needed** - Context7 has latest info

## Version History

**v1.0.0 (2026-01-01)** - Initial release with library resolution, documentation querying, reference creation, skill integration patterns, and Context7 MCP integration

## Sources

- [Context7 Official](https://context7.com)
- [Context7 GitHub](https://github.com/context7)
- MCP Protocol Documentation
- Official library documentation sources
