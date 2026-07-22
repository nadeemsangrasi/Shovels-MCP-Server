# Examples

## Example 1: New Library Integration

### Goal
Integrate a new library (e.g., "zod") into a project.

### Workflow

**Step 1: Resolve Library ID**
```
mcp__context7__resolve-library-id("zod", "zod validation schema")
```

**Step 2: Query Documentation**
```
mcp__context7__query-docs("/colinhacks/zod", "zod schema validation TypeScript")
```

**Step 3: Create Reference**
```markdown
# Zod Validation Reference

## Source
- Context7 ID: /colinhacks/zod
- Query: "zod schema validation TypeScript"

## Zod Basics
- Define schemas with zod.object(), zod.string(), etc.
- Parse data with schema.parse()
- Type inference with infer<typeof schema>

## Code Examples

### Basic Schema
```typescript
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  age: z.number().min(0).optional(),
});

type User = z.infer<typeof UserSchema>;
```

### Validation
```typescript
const result = UserSchema.safeParse(data);
if (!result.success) {
  console.log(result.error.format());
}
```
```

## Example 2: Feature Implementation

### Goal
Implement authentication with JWT in a FastAPI backend.

### Workflow

**Step 1: Resolve Library**
```
mcp__context7__resolve-library-id("python-jwt", "FastAPI JWT authentication")
```

**Step 2: Query Specific Feature**
```
mcp__context7__query-docs("/fastapi/fastapi", "FastAPI OAuth2Bearer JWT dependency")
```

**Step 3: Apply Code**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
```

## Example 3: Troubleshooting

### Goal
Fix Next.js 14 dynamic route 404 issue.

### Workflow

**Step 1: Query the Issue**
```
mcp__context7__resolve-library-id("nextjs", "nextjs dynamic route")
mcp__context7__query-docs("/vercel/next.js", "Next.js dynamic route 404 not found")
```

**Step 2: Find Solution**
Common issue: Route params not being passed correctly.

**Step 3: Apply Fix**
```tsx
// Before (broken)
export default function Page({ params }: { params: { id: string } }) {
  return <div>{params.id}</div>;  // params might be empty
}

// After (fixed)
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <div>{id}</div>;
}
```

## Example 4: Migration

### Goal
Migrate from React class components to hooks.

### Workflow

**Step 1: Resolve Library**
```
mcp__context7__resolve-library-id("react", "react hooks useEffect")
```

**Step 2: Query Migration Patterns**
```
mcp__context7__query-docs("/facebook/react", "React class component to hooks migration")
```

**Step 3: Apply Patterns**
```tsx
// Before (Class)
class User extends React.Component {
  componentDidMount() {
    this.fetchData();
  }

  render() {
    return <div>{this.props.user.name}</div>;
  }
}

// After (Hooks)
function User({ userId }) {
  useEffect(() => {
    fetchData(userId);
  }, [userId]);

  return <div>{user?.name}</div>;
}
```

## Example 5: Skill Enhancement

### Goal
Enhance a skill with current documentation.

### Workflow

**Step 1: Identify Gap**
Skill has outdated FastAPI patterns.

**Step 2: Fetch Current Docs**
```
mcp__context7__resolve-library-id("fastapi", "fastapi 0.109 new features")
mcp__context7__query-docs("/fastapi/fastapi", "FastAPI latest version new features")
```

**Step 3: Update Skill**
Add new patterns to skill's references.

**Step 4: Document Source**
```
## Updated
- Added OpenAPI 3.1 support
- Updated dependency injection patterns
- Source: Context7 /fastapi/fastapi (2024-01)
```
