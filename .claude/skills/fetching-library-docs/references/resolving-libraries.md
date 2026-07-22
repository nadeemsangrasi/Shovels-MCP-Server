# Resolving Library IDs

## Understanding Library Resolution

Context7 uses a library ID system to uniquely identify documentation sources. The `resolve-library-id` tool maps library/package names to Context7-compatible IDs.

## How It Works

```json
{
  "libraryName": "package-name",
  "query": "what you want to accomplish"
}
```

Returns library candidates with:
- **Library ID:** Format `/org/project` or `/org/project/version`
- **Benchmark Score:** Quality indicator (0-100)
- **Code Snippets:** Number of examples available
- **Source Reputation:** High/Medium/Low

## Common Library Patterns

### JavaScript/TypeScript Libraries

| Package | Library ID | Benchmark |
|---------|------------|-----------|
| react | `/facebook/react` | 85.2 |
| nextjs | `/vercel/next.js` | 87.1 |
| express | `/expressjs/express` | 78.5 |
| fastify | `/fastify/fastify` | 82.3 |
| axios | `/axios/axios` | 75.0 |
| lodash | `/lodash/lodash` | 72.1 |

### Python Libraries

| Package | Library ID | Benchmark |
|---------|------------|-----------|
| fastapi | `/fastapi/fastapi` | 87.2 |
| django | `/django/django` | 84.5 |
| flask | `/pallets/flask` | 79.3 |
| sqlalchemy | `/sqlalchemy/sqlalchemy` | 81.0 |
| pandas | `/pandas-dev/pandas` | 83.7 |

### DevOps/Containers

| Tool | Library ID | Benchmark |
|------|------------|-----------|
| docker | `/docker/docs` | 84.3 |
| kubernetes | `/kubernetes/kubernetes` | 86.1 |
| nginx | `/nginx/nginx` | 77.5 |

### Authentication

| Library | Library ID | Benchmark |
|---------|------------|-----------|
| better-auth | `/better-auth/better-auth` | 72.3 |
| nextauth | `/nextauthjs/next-auth` | 80.2 |
| auth0 | `/auth0/auth0` | 79.8 |

## Query Strategies

### Basic Query
```json
{
  "libraryName": "fastapi",
  "query": "fastapi documentation"
}
```

### Specific Task Query
```json
{
  "libraryName": "react",
  "query": "hooks state management"
}
```

### Framework Query
```json
{
  "libraryName": "nextjs",
  "query": "app router server components"
}
```

## Selection Criteria

### Choose Based On:

1. **Benchmark Score** - Higher is better (closer to 100)
2. **Code Snippets** - More examples = more useful
3. **Source Reputation** - Official docs preferred
4. **Version Availability** - Check if version needed

### Example Selection

```json
[
  {
    "libraryId": "/fastapi/fastapi",
    "benchmark": 87.2,
    "snippets": 881,
    "reputation": "High"
  },
  {
    "libraryId": "/websites/fastapi_tiangolo",
    "benchmark": 79.8,
    "snippets": 31710,
    "reputation": "High"
  }
]
```

Choose `/fastapi/fastapi` for official API reference.

## Version-Specific Queries

```json
{
  "libraryName": "nextjs",
  "query": "nextjs 14 app router"
}
```

Results may include version-specific IDs like `/vercel/next.js/v14.3.0`.

## Troubleshooting

### No Results
- Try alternative package names
- Check spelling
- Try broader query terms

### Wrong Library
- Add more specific query
- Check benchmark scores
- Look for official documentation

### Multiple Options
- Compare benchmark scores
- Check snippet counts
- Prefer official sources
