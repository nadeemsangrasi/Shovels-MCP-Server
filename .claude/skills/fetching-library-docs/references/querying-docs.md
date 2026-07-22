# Querying Documentation

## Query Structure

```json
{
  "libraryId": "/org/project",
  "query": "specific question about the library"
}
```

## Query Best Practices

### Be Specific

**Good queries:**
- "How to create a REST endpoint in FastAPI"
- "React useState with TypeScript typing"
- "Docker multi-stage build Python application"
- "Next.js 14 dynamic routes parameters"

**Bad queries:**
- "FastAPI docs" (too vague)
- "React everything" (too broad)
- "Docker guide" (not specific)

### Task-Oriented

Frame queries around tasks:

| Task | Example Query |
|------|---------------|
| Create endpoint | "FastAPI POST endpoint with validation" |
| Handle state | "React useState initial value function" |
| Configure build | "Docker compose multi-container setup" |
| Fetch data | "Next.js 14 server actions form submission" |

### Include Context

```json
{
  "libraryId": "/fastapi/fastapi",
  "query": "authentication JWT token verification dependency"
}
```

## Query Categories

### Implementation Queries

```json
{
  "libraryId": "/react",
  "query": "React.forwardRef with TypeScript example"
}
```

### Comparison Queries

```json
{
  "libraryId": "/fastapi/fastapi",
  "query": "FastAPI vs Express routing comparison"
}
```

### Best Practice Queries

```json
{
  "libraryId": "/docker/docs",
  "query": "Dockerfile best practices production security"
}
```

### Troubleshooting Queries

```json
{
  "libraryId": "/nextjs",
  "query": "Next.js dynamic route 404 not found solution"
}
```

### Pattern Queries

```json
{
  "libraryId": "/react",
  "query": "React component patterns 2024"
}
```

## Processing Results

### Understanding Output

Context7 returns:
1. **Code snippets** - Most useful for implementation
2. **Explanations** - Context and usage
3. **Links** - Reference to full documentation

### Extracting Information

```markdown
## From Documentation

### Key Concepts
- Concept 1: What it does
- Concept 2: How it works

### Code Example
```language
// Copy from result
code here
```

### Important Notes
- Note 1
- Note 2
```

### Saving Reference

Create `.claude/skills/library/references/feature.md`:

```markdown
# Library Feature Reference

## Source
- Context7 ID: /org/project
- Query: "your query"
- Date: 2024-01-01

## Feature Description

## Code Example

## Usage Notes

## Related
```

## Query Limits

- Maximum 3 queries per question
- Use best query on first attempt
- Refine if results not helpful

## Refining Queries

### If Results Are Too General

Add more specific terms:
```
Before: "React hooks"
After: "React useEffect cleanup function example"
```

### If Results Are Empty

Try broader terms:
```
Before: "Next.js app router middleware auth"
After: "Next.js middleware authentication"
```

### If Results Are Wrong Library

Re-resolve library ID:
```
mcp__context7__resolve-library-id("next-auth", "authentication nextjs")
```

## Common Query Templates

### API/Endpoint

```
"{library} {method} request {task}"
// Example: "FastAPI POST request form validation"
```

### Component/Pattern

```
"{library} {component} {task} {framework}"
// Example: "React component TypeScript props"
```

### Configuration

```
"{library} {configuration} {environment}"
// Example: "Docker compose production configuration"
```

### Error Resolution

```
"{library} {error_type} {solution}"
// Example: "React useEffect strict mode warning"
```
