# Fetching Library Docs with Context7 MCP

A comprehensive Claude Code skill for fetching up-to-date official documentation and code examples using Context7 MCP. Get accurate, version-specific library information for any project.

## Overview

This skill provides a complete workflow for using Context7 MCP to:
- Find the right library documentation
- Fetch official documentation and examples
- Create reusable reference materials
- Integrate documentation into existing skills

## Features

### Library Resolution
- Find Context7 library IDs for any package
- Compare benchmark scores and snippet counts
- Select the best documentation source
- Handle version-specific queries

### Documentation Fetching
- Query specific features and patterns
- Get code examples from official docs
- Extract key concepts and patterns
- Process results efficiently

### Reference Creation
- Create project-specific reference files
- Document patterns for future use
- Version control for documentation
- Cross-reference skills

### Skill Integration
- Link Context7 docs to existing skills
- Enhance skills with current information
- Create integration sub-references
- Maintain up-to-date documentation

## Installation

```bash
cp -r fetching-library-docs /path/to/project/.claude/skills/
```

## Usage

### Activation

Trigger keywords:
- "context7", "fetch docs"
- "library documentation", "api reference"
- "code examples", "official docs"
- "get documentation", "learn library"

### Example Prompts

**Basic Queries:**
- "Fetch docs for FastAPI"
- "Get React useEffect examples"
- "Show me Docker multi-stage build patterns"

**Specific Tasks:**
- "How to create a FastAPI endpoint with validation"
- "React useState with TypeScript typing"
- "Next.js 14 app router data fetching"

**Troubleshooting:**
- "Fix Next.js dynamic route 404"
- "React useEffect cleanup examples"

## Documentation Structure

```
fetching-library-docs/
├── SKILL.md (492 lines)              # Main workflow
├── README.md                          # This file
├── references/
│   ├── resolving-libraries.md         # Finding library IDs
│   ├── querying-docs.md               # Query strategies
│   ├── creating-references.md         # Reference templates
│   ├── skill-integration.md           # Cross-skill linking
│   ├── examples.md                    # Usage examples
│   └── troubleshooting.md             # Common issues
├── assets/templates/
└── scripts/
```

## Key Concepts

### MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp__context7__resolve-library-id` | Find library ID from package name |
| `mcp__context7__query-docs` | Get documentation for specific features |

### Workflow

```
1. Resolve Library → 2. Query Docs → 3. Create Reference → 4. Integrate
```

### Query Patterns

**Good Queries:**
- "How to create a REST endpoint in FastAPI"
- "React useState with TypeScript typing"
- "Docker multi-stage build Python application"

**Bad Queries:**
- "FastAPI docs" (too vague)
- "React everything" (too broad)

## Common Use Cases

### New Library Integration
Resolve library ID → Query docs → Create reference → Implement

### Feature Implementation
Query specific feature → Get code examples → Apply pattern

### Troubleshooting
Query error → Get solution from docs → Apply fix

### Version Migration
Query version-specific docs → Compare patterns → Update code

## Integration with Other Skills

### Works With
- **better-auth-nextjs** → Fetch Better Auth docs
- **scaffolding-fastapi** → Fetch FastAPI docs
- **docker-containerization** → Fetch Docker docs
- **nextjs16** → Fetch Next.js docs
- **styling-with-shadcn** → Fetch shadcn/ui docs

### Enhancement Pattern
1. Identify documentation gap in skill
2. Use Context7 to fetch current docs
3. Create sub-reference in skill's references
4. Update skill to link to new reference

## Tools Covered

**Context7 MCP:**
- Library resolution
- Documentation querying
- Code snippet extraction
- Version-specific queries

**Reference Management:**
- Template-based creation
- Version tracking
- Cross-referencing
- Skill integration

## Requirements

**Knowledge:**
- Package/library names
- What you want to accomplish
- Basic documentation reading

**Tools:**
- Context7 MCP configured
- Access to code editor

## Resources

**Local Documentation:**
- Resolving libraries: `references/resolving-libraries.md`
- Querying docs: `references/querying-docs.md`
- Creating references: `references/creating-references.md`
- Examples: `references/examples.md`

**External:**
- [Context7 Official](https://context7.com)
- [MCP Protocol](https://modelcontextprotocol.io)

## Best Practices

1. **Start specific** - Begin with library resolution
2. **Be detailed** - Specific queries get better results
3. **Save references** - Create files for future use
4. **Test examples** - Verify code from docs works
5. **Link sources** - Document where info came from
6. **Re-query when needed** - Context7 has latest info

## Tips for Success

1. **Use package names** - "react" not "React.js"
2. **Describe the task** - "validation" not "docs"
3. **Check benchmark** - Higher score = better quality
4. **Create references** - Saves time later
5. **Integrate skills** - Link to existing skills
6. **Version matters** - Use version-specific IDs

## Version History

**v1.0.0 (2026-01-01)**
- Initial release
- Library resolution workflow
- Documentation querying
- Reference creation
- Skill integration patterns
- Progressive disclosure structure (492 lines)

## Support

- [Context7 GitHub](https://github.com/context7)
- [MCP Documentation](https://modelcontextprotocol.io)

## Contributing

Improvements welcome! Please ensure:
- SKILL.md stays under 500 lines
- Examples are accurate
- References are up-to-date
- Integration patterns work

---

**Created with:** Claude Code + skill-creator + Context7 MCP
**Documentation Quality:** Production-ready
**Maintenance:** Self-contained, version 1.0.0
