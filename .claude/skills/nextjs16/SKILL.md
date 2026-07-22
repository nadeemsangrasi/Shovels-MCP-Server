---
name: nextjs16
description: Build Next.js 16 applications with App Router, Server Components, Server Actions, and modern React features. Use when creating Next.js apps, implementing routing, data fetching, or working with React Server Components.
version: 1.0.0
allowed-tools: Bash, Read, Write, Edit, mcp__context7__query-docs, mcp__context7__resolve-library-id
author: Skill Creator
tags: [nextjs, react, web-development, full-stack, app-router, server-components]
---

# Next.js 16 Development Skill

## Overview

Build modern Next.js 16 applications using App Router, React Server Components, Server Actions, and advanced caching. This skill leverages Context7 MCP for up-to-date official documentation.

**Core Features:**
- App Router with file-based routing
- Server Components (default) + Client Components
- Server Actions for mutations
- Advanced caching strategies
- Loading states and error boundaries

## When to Use This Skill

**Activate when:**
- Creating new Next.js 16 applications
- Implementing App Router routing
- Building with Server Components
- Adding Server Actions for forms
- Need official Next.js 16 documentation

**Trigger keywords:** "Next.js", "App Router", "Server Components", "Server Actions", "Next.js routing"

## Prerequisites

**Required:**
- Node.js 18.17+
- npm/yarn/pnpm
- React knowledge
- Context7 MCP configured

**Recommended:**
- TypeScript
- Async/await understanding

## Instructions

### Phase 1: Project Setup

#### Step 1: Create Next.js Application

**New project:**
```bash
npx create-next-app@latest my-app
# Select: TypeScript ✓, ESLint ✓, App Router ✓ (required)
cd my-app
```

**Verify structure:**
```
app/
├── layout.tsx    # Root layout (required)
├── page.tsx      # Home page
└── ...
```

**Validation:**
- [ ] `app/layout.tsx` has `<html>` and `<body>` tags
- [ ] `package.json` shows `next@16.x`

#### Step 2: Start Development Server

```bash
npm run dev
# Visit http://localhost:3000
```

### Phase 2: Routing & Layouts

#### Step 3: Create Routes

**File-based routing:**
```
app/
├── page.tsx                    # /
├── about/page.tsx             # /about
├── blog/
│   ├── page.tsx               # /blog
│   └── [slug]/page.tsx        # /blog/:slug
└── dashboard/
    ├── layout.tsx             # Shared layout
    └── page.tsx               # /dashboard
```

**Dynamic route example:**
```typescript
// app/blog/[slug]/page.tsx
export default function Post({ params }: { params: { slug: string } }) {
  return <h1>Post: {params.slug}</h1>
}
```

**See:** `references/routing.md` for complete conventions

#### Step 4: Implement Layouts

**Root layout (required):**
```typescript
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav>{/* Navigation */}</nav>
        {children}
      </body>
    </html>
  )
}
```

**Nested layout:**
```typescript
// app/dashboard/layout.tsx
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <aside>{/* Sidebar */}</aside>
      <main>{children}</main>
    </div>
  )
}
```

**Key:** Layouts persist across navigation, nest automatically

### Phase 3: Data Fetching

#### Step 5: Fetch in Server Components

**Choose strategy based on data freshness:**

```typescript
// Static (default) - cached indefinitely
const data = await fetch('https://...', { cache: 'force-cache' })

// Dynamic - always fresh
const data = await fetch('https://...', { cache: 'no-store' })

// Revalidated - cached with TTL
const data = await fetch('https://...', { next: { revalidate: 3600 } })

// Tagged - revalidate on-demand
const data = await fetch('https://...', { next: { tags: ['posts'] } })
```

**Example page with data:**
```typescript
// app/blog/page.tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts')
  if (!res.ok) throw new Error('Failed to fetch')
  return res.json()
}

export default async function BlogPage() {
  const posts = await getPosts()
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

**See:** `references/official-docs/data-fetching.md` for all patterns

### Phase 4: Client Components

#### Step 6: Add Interactivity

**When to use Client Components:**
- Interactive features (onClick, onChange)
- React hooks (useState, useEffect)
- Browser APIs (localStorage, window)

**Create Client Component:**
```typescript
// app/components/Counter.tsx
'use client' // Required directive

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

**Compose Server + Client:**
```typescript
// app/page.tsx (Server Component)
import { Counter } from './components/Counter'

async function getData() {
  return fetch('https://...').then(r => r.json())
}

export default async function Page() {
  const data = await getData() // Fetch on server
  return (
    <div>
      <h1>{data.title}</h1>
      <Counter /> {/* Interactive on client */}
    </div>
  )
}
```

**Best practice:** Keep Client Components small and deep in tree

**See:** `references/official-docs/components.md` for composition patterns

### Phase 5: Server Actions

#### Step 7: Implement Forms & Mutations

**Create Server Action:**
```typescript
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await db.post.create({ data: { title, content } })

  revalidatePath('/posts')
  redirect('/posts')
}
```

**Use in form:**
```typescript
// app/posts/new/page.tsx
import { createPost } from '@/app/actions'

export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create</button>
    </form>
  )
}
```

**With loading state (Client Component):**
```typescript
'use client'
import { useFormStatus } from 'react-dom'

function SubmitButton() {
  const { pending } = useFormStatus()
  return <button disabled={pending}>{pending ? 'Saving...' : 'Save'}</button>
}
```

**See:** `references/official-docs/server-actions.md` for advanced patterns

### Phase 6: Loading & Error States

#### Step 8: Add Loading UI

**Create loading.tsx:**
```typescript
// app/blog/loading.tsx
export default function Loading() {
  return <div>Loading posts...</div>
}
```

Auto-wraps page in Suspense boundary

#### Step 9: Add Error Boundaries

**Create error.tsx:**
```typescript
// app/blog/error.tsx
'use client' // Must be Client Component

export default function Error({ error, reset }: {
  error: Error
  reset: () => void
}) {
  return (
    <div>
      <h2>Error: {error.message}</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

**Programmatic not-found:**
```typescript
import { notFound } from 'next/navigation'

export default async function Post({ params }) {
  const post = await getPost(params.slug)
  if (!post) notFound() // Renders not-found.tsx
  return <article>{post.title}</article>
}
```

### Phase 7: Navigation

#### Step 10: Implement Client-Side Navigation

**Link component (automatic prefetching):**
```typescript
import Link from 'next/link'

export function Nav() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/blog">Blog</Link>
    </nav>
  )
}
```

**Programmatic navigation:**
```typescript
'use client'
import { useRouter } from 'next/navigation'

export function BackButton() {
  const router = useRouter()
  return <button onClick={() => router.back()}>Back</button>
}
```

### Phase 8: Access Documentation

#### Step 11: Query Official Docs

**When you need specific documentation:**

1. Use Context7 MCP with library ID: `/vercel/next.js/v16.1.0`
2. Query for specific topics: routing, data fetching, APIs, etc.
3. Check local references first:
   - `references/official-docs/data-fetching.md`
   - `references/official-docs/routing.md`
   - `references/official-docs/components.md`
   - `references/official-docs/server-actions.md`
4. See `references/examples.md` for complete project patterns
5. See `references/quick-reference.md` for common snippets

## Common Patterns

### Static Blog
- Use Server Components with `cache: 'force-cache'`
- Dynamic routes: `[slug]/page.tsx`
- See: `references/examples.md#static-blog`

### Real-Time Dashboard
- Server Component for initial data
- Client Components for interactivity
- Use `cache: 'no-store'` for fresh data
- See: `references/examples.md#dashboard`

### E-commerce
- ISR with `revalidate: 3600`
- Server Actions for cart/checkout
- See: `references/examples.md#ecommerce`

### Authentication
- Server Actions for login/signup
- Middleware for protected routes
- See: `references/examples.md#authentication`

## Error Handling

**Common errors:**

| Error | Solution |
|-------|----------|
| "needs useState" | Add `'use client'` directive |
| "fetch failed" | Check API, add error handling, use error.tsx |
| "Route not found" | Ensure `page.tsx` exists (not just folder) |
| "createContext not a function" | Move context to Client Component |

**Debug tips:**
1. Check Server vs Client Components (hooks only in Client)
2. Verify file names: `page.tsx` (lowercase)
3. Clear cache: `rm -rf .next && npm run dev`
4. Check fetch caching with Network tab

**See:** `references/troubleshooting.md` for complete guide

## Limitations

**Server Components cannot:**
- Use React hooks
- Handle browser events
- Access browser APIs

**Client Components:**
- Add to bundle size
- Require hydration
- Cannot be async functions

**Server Actions:**
- Must be marked `'use server'`
- Props must be serializable
- Cannot skip middleware

## Validation Checklist

Before deploying:

**Structure:**
- [ ] Root layout has html/body tags
- [ ] All routes have page.tsx
- [ ] Loading/error states added
- [ ] 404 page exists

**Performance:**
- [ ] Images use next/image
- [ ] Appropriate caching applied
- [ ] Server Components used by default
- [ ] Client Components minimized

**Data:**
- [ ] Fetch includes cache options
- [ ] Error handling implemented
- [ ] Revalidation configured

**Forms:**
- [ ] Server Actions marked properly
- [ ] Validation implemented
- [ ] Loading states shown

## Decision Trees

### Server vs Client Component?
```
Need interactivity? → Client Component ('use client')
Use React hooks? → Client Component
Access browser APIs? → Client Component
Fetch data? → Server Component (default)
Otherwise → Server Component (default)
```

### Caching Strategy?
```
Rarely changes? → cache: 'force-cache' (default)
User-specific? → cache: 'no-store'
Periodic updates? → revalidate: N seconds
Event-based? → tags: ['name'] + revalidateTag()
```

## References

**Local Documentation:**
- Complete routing guide: `references/official-docs/routing.md`
- Data fetching patterns: `references/official-docs/data-fetching.md`
- Component types: `references/official-docs/components.md`
- Server Actions: `references/official-docs/server-actions.md`
- Example projects: `references/examples.md`
- Quick reference: `references/quick-reference.md`
- Troubleshooting: `references/troubleshooting.md`

**Context7 Library:**
- Library ID: `/vercel/next.js/v16.1.0`
- Query for latest documentation

**External:**
- Official Docs: https://nextjs.org/docs
- GitHub: https://github.com/vercel/next.js
- Examples: https://github.com/vercel/next.js/tree/canary/examples

## Tips for Success

1. **Start with Server Components** - Only add `'use client'` when needed
2. **Choose right caching** - Static by default, dynamic when needed
3. **Compose wisely** - Server (data) → Client (interaction) → Server (more data)
4. **Use Context7** - Query `/vercel/next.js/v16.1.0` for latest docs
5. **Check references first** - Most answers in local docs

## Version History

**v1.0.0 (2026-01-01)**
- Initial release
- Next.js 16.1.0 support
- Complete App Router coverage
- Context7 integration
- Progressive disclosure optimization
