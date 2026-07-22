# Next.js 16 Routing and File Conventions

This document contains official Next.js 16 App Router conventions and routing patterns fetched from Context7.

## Overview

Next.js 16 uses a file-system based router where folders define routes and special files create UI, loading states, and error handling. The App Router is built on React Server Components and supports advanced features like nested layouts, parallel routes, and intercepting routes.

## File Conventions

### Core Files

| File | Purpose | Required |
|------|---------|----------|
| `layout.tsx` | Shared UI for a route segment and its children | Required for root |
| `page.tsx` | Unique UI for a route, makes it publicly accessible | Required for route |
| `loading.tsx` | Loading UI for a route segment | Optional |
| `error.tsx` | Error boundary for a route segment | Optional |
| `not-found.tsx` | Not found UI for a route segment | Optional |
| `route.ts` | API endpoint (Route Handler) | Optional |
| `template.tsx` | Re-rendered layout (not cached) | Optional |
| `default.tsx` | Fallback page for Parallel Routes | Optional |

## Basic Routing

### Creating Routes

Routes are defined by folder structure:

```
app/
├── page.tsx                    # Route: /
├── about/
│   └── page.tsx               # Route: /about
├── blog/
│   ├── page.tsx               # Route: /blog
│   └── [slug]/
│       └── page.tsx           # Route: /blog/:slug
└── dashboard/
    ├── layout.tsx
    ├── page.tsx               # Route: /dashboard
    └── settings/
        └── page.tsx           # Route: /dashboard/settings
```

### Simple Page

```typescript
// app/about/page.tsx
export default function AboutPage() {
  return (
    <div>
      <h1>About Us</h1>
      <p>Welcome to our application.</p>
    </div>
  )
}
```

## Layouts

### Root Layout (Required)

The root layout is **required** and must contain `<html>` and `<body>` tags:

```typescript
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <header>
          <nav>{/* Navigation */}</nav>
        </header>
        <main>{children}</main>
        <footer>{/* Footer */}</footer>
      </body>
    </html>
  )
}
```

**Key Points:**
- Must include `<html>` and `<body>` tags
- Replaces `_app.tsx` and `_document.tsx` from Pages Router
- Cannot be a Client Component
- Shared across all routes
- Persists across navigations (no re-render)

### Nested Layouts

Create layouts for specific route segments:

```typescript
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="dashboard">
      <aside>
        <nav>
          <Link href="/dashboard">Overview</Link>
          <Link href="/dashboard/settings">Settings</Link>
          <Link href="/dashboard/profile">Profile</Link>
        </nav>
      </aside>
      <section className="content">
        {children}
      </section>
    </div>
  )
}

// app/dashboard/page.tsx
export default function DashboardPage() {
  return <h1>Dashboard Overview</h1>
}
```

**Layout Composition:**
```
RootLayout
  └─ DashboardLayout
       └─ DashboardPage
```

Layouts automatically nest and persist across route changes within their segment.

### Templates

Templates are similar to layouts but re-render on navigation:

```typescript
// app/template.tsx
export default function Template({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}
```

**Use templates when you need:**
- CSS/JS animations on route changes
- Fresh component instances on navigation
- Behavior that requires re-mounting

## Dynamic Routes

### Single Dynamic Segment

```typescript
// app/blog/[slug]/page.tsx
export default function BlogPost({
  params,
}: {
  params: { slug: string }
}) {
  return <h1>Post: {params.slug}</h1>
}
```

**URL matches:**
- `/blog/hello-world` → `params.slug = "hello-world"`
- `/blog/nextjs-guide` → `params.slug = "nextjs-guide"`

### Multiple Dynamic Segments

```typescript
// app/shop/[category]/[product]/page.tsx
export default function ProductPage({
  params,
}: {
  params: { category: string; product: string }
}) {
  return (
    <div>
      <h1>Category: {params.category}</h1>
      <h2>Product: {params.product}</h2>
    </div>
  )
}
```

**URL matches:**
- `/shop/electronics/laptop` → `{ category: "electronics", product: "laptop" }`

### Catch-All Segments

```typescript
// app/docs/[...slug]/page.tsx
export default function DocsPage({
  params,
}: {
  params: { slug: string[] }
}) {
  return <div>Docs path: {params.slug.join('/')}</div>
}
```

**URL matches:**
- `/docs/intro` → `params.slug = ["intro"]`
- `/docs/getting-started/installation` → `params.slug = ["getting-started", "installation"]`
- Does NOT match `/docs` (use optional catch-all for that)

### Optional Catch-All Segments

```typescript
// app/shop/[[...slug]]/page.tsx
export default function ShopPage({
  params,
}: {
  params: { slug?: string[] }
}) {
  if (!params.slug) {
    return <div>Shop Home</div>
  }

  return <div>Path: {params.slug.join('/')}</div>
}
```

**URL matches:**
- `/shop` → `params.slug = undefined`
- `/shop/electronics` → `params.slug = ["electronics"]`
- `/shop/electronics/laptops` → `params.slug = ["electronics", "laptops"]`

## Route Groups

Organize routes without affecting URL structure using `(folder)`:

```
app/
├── (marketing)/
│   ├── layout.tsx         # Shared marketing layout
│   ├── about/
│   │   └── page.tsx       # Route: /about
│   └── contact/
│       └── page.tsx       # Route: /contact
└── (shop)/
    ├── layout.tsx         # Shared shop layout
    ├── products/
    │   └── page.tsx       # Route: /products
    └── cart/
        └── page.tsx       # Route: /cart
```

**Benefits:**
- Organize code by feature/section
- Apply different layouts to route groups
- Multiple root layouts in same app

## Loading States

### Automatic Loading UI

Create `loading.tsx` to show UI while route segment loads:

```typescript
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="skeleton">
      <div className="skeleton-header" />
      <div className="skeleton-content" />
    </div>
  )
}

// app/dashboard/page.tsx
export default async function DashboardPage() {
  const data = await fetch('...').then(r => r.json())
  return <div>{data.content}</div>
}
```

**How it works:**
- Next.js automatically wraps `page.tsx` in a React Suspense boundary
- `loading.tsx` is shown while data is being fetched
- Instant loading state without manual Suspense

### Manual Suspense

For more control, use Suspense boundaries:

```typescript
import { Suspense } from 'react'

async function Analytics() {
  const data = await fetch('...', { cache: 'no-store' })
  return <div>{/* Analytics UI */}</div>
}

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<div>Loading analytics...</div>}>
        <Analytics />
      </Suspense>
      {/* Rest of page renders immediately */}
    </div>
  )
}
```

## Error Handling

### Error Boundaries

Create `error.tsx` to handle errors in a route segment:

```typescript
// app/dashboard/error.tsx
'use client' // Error boundaries must be Client Components

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

**Key Points:**
- Must be a Client Component (`'use client'`)
- Receives `error` object and `reset` function
- Catches errors in nested routes and components
- Does NOT catch errors in `layout.tsx` of same segment

### Global Error Boundary

For root layout errors, create `global-error.tsx`:

```typescript
// app/global-error.tsx
'use client'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html>
      <body>
        <h2>Something went wrong!</h2>
        <button onClick={reset}>Try again</button>
      </body>
    </html>
  )
}
```

### Not Found Pages

Create custom 404 pages with `not-found.tsx`:

```typescript
// app/blog/[slug]/not-found.tsx
export default function NotFound() {
  return (
    <div>
      <h2>Post Not Found</h2>
      <p>The blog post you're looking for doesn't exist.</p>
      <Link href="/blog">View all posts</Link>
    </div>
  )
}

// Trigger programmatically
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation'

async function getPost(slug: string) {
  const res = await fetch(`https://api.example.com/posts/${slug}`)
  if (!res.ok) return null
  return res.json()
}

export default async function PostPage({
  params,
}: {
  params: { slug: string }
}) {
  const post = await getPost(params.slug)

  if (!post) {
    notFound() // Renders not-found.tsx
  }

  return <article>{post.title}</article>
}
```

## Navigation

### Link Component

Client-side navigation with automatic prefetching:

```typescript
import Link from 'next/link'

export default function Navigation() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <Link href="/blog">Blog</Link>

      {/* With dynamic routes */}
      <Link href="/blog/hello-world">Hello World Post</Link>

      {/* With query params */}
      <Link href={{ pathname: '/search', query: { q: 'nextjs' } }}>
        Search
      </Link>
    </nav>
  )
}
```

**Features:**
- Automatic prefetching in viewport
- Client-side navigation (no full page reload)
- Scroll restoration
- Focus management

### useRouter Hook

Programmatic navigation in Client Components:

```typescript
'use client'

import { useRouter } from 'next/navigation'

export function BackButton() {
  const router = useRouter()

  return (
    <div>
      <button onClick={() => router.back()}>Go Back</button>
      <button onClick={() => router.push('/dashboard')}>
        Go to Dashboard
      </button>
      <button onClick={() => router.refresh()}>Refresh</button>
    </div>
  )
}
```

**Available methods:**
- `router.push(href)` - Navigate to route
- `router.replace(href)` - Replace current route
- `router.back()` - Navigate back
- `router.forward()` - Navigate forward
- `router.refresh()` - Refresh current route
- `router.prefetch(href)` - Prefetch route

### usePathname Hook

Get current pathname in Client Components:

```typescript
'use client'

import { usePathname } from 'next/navigation'
import Link from 'next/link'

export function Navigation() {
  const pathname = usePathname()

  return (
    <nav>
      <Link
        href="/"
        className={pathname === '/' ? 'active' : ''}
      >
        Home
      </Link>
      <Link
        href="/about"
        className={pathname === '/about' ? 'active' : ''}
      >
        About
      </Link>
    </nav>
  )
}
```

### useSearchParams Hook

Access URL search params in Client Components:

```typescript
'use client'

import { useSearchParams } from 'next/navigation'

export function SearchResults() {
  const searchParams = useSearchParams()
  const query = searchParams.get('q')

  return <div>Search results for: {query}</div>
}
```

### redirect Function

Server-side redirects:

```typescript
import { redirect } from 'next/navigation'

export default async function Page() {
  const session = await getSession()

  if (!session) {
    redirect('/login')
  }

  return <div>Protected content</div>
}
```

## Route Handlers (API Routes)

Create API endpoints with `route.ts`:

```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'

// GET /api/posts
export async function GET(request: NextRequest) {
  const posts = await db.posts.findMany()
  return NextResponse.json(posts)
}

// POST /api/posts
export async function POST(request: NextRequest) {
  const body = await request.json()
  const post = await db.posts.create({ data: body })
  return NextResponse.json(post, { status: 201 })
}
```

**Dynamic routes in Route Handlers:**

```typescript
// app/api/posts/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const post = await db.posts.findUnique({
    where: { id: params.id }
  })

  if (!post) {
    return NextResponse.json(
      { error: 'Post not found' },
      { status: 404 }
    )
  }

  return NextResponse.json(post)
}
```

## Metadata

### Static Metadata

```typescript
// app/about/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn more about our company',
}

export default function AboutPage() {
  return <div>About content</div>
}
```

### Dynamic Metadata

```typescript
// app/blog/[slug]/page.tsx
import { Metadata } from 'next'

export async function generateMetadata({
  params,
}: {
  params: { slug: string }
}): Promise<Metadata> {
  const post = await fetch(`https://api.example.com/posts/${params.slug}`)
    .then(r => r.json())

  return {
    title: post.title,
    description: post.excerpt,
  }
}

export default function BlogPost({ params }: { params: { slug: string } }) {
  return <article>{/* Post content */}</article>
}
```

## Best Practices

### 1. Use Layouts for Shared UI

```typescript
// ✅ Good: Shared navigation in layout
// app/dashboard/layout.tsx
export default function Layout({ children }) {
  return (
    <>
      <DashboardNav />
      {children}
    </>
  )
}
```

### 2. Colocate Files

Keep related files close to where they're used:

```
app/
└── dashboard/
    ├── layout.tsx
    ├── page.tsx
    ├── components/
    │   ├── DashboardCard.tsx
    │   └── StatsWidget.tsx
    └── lib/
        └── analytics.ts
```

### 3. Use Loading States

Always provide loading UI for async data:

```typescript
// app/dashboard/loading.tsx
export default function Loading() {
  return <LoadingSkeleton />
}
```

### 4. Handle Errors Gracefully

Add error boundaries to catch runtime errors:

```typescript
// app/dashboard/error.tsx
'use client'

export default function Error({ error, reset }) {
  return (
    <div>
      <h2>Failed to load dashboard</h2>
      <button onClick={reset}>Retry</button>
    </div>
  )
}
```

### 5. Organize with Route Groups

```
app/
├── (marketing)/
│   ├── layout.tsx
│   └── ...
└── (app)/
    ├── layout.tsx
    └── ...
```

## Migration from Pages Router

### Pages → App Router

| Pages Router | App Router |
|--------------|------------|
| `pages/index.tsx` | `app/page.tsx` |
| `pages/about.tsx` | `app/about/page.tsx` |
| `pages/blog/[slug].tsx` | `app/blog/[slug]/page.tsx` |
| `pages/_app.tsx` | `app/layout.tsx` |
| `pages/_document.tsx` | `app/layout.tsx` |
| `pages/_error.tsx` | `app/error.tsx` |
| `pages/404.tsx` | `app/not-found.tsx` |
| `pages/api/posts.ts` | `app/api/posts/route.ts` |

## Summary

Next.js 16 App Router provides:
- **File-based routing** with folder structure
- **Nested layouts** that persist and compose
- **Loading and error states** with special files
- **Server Components** as default
- **Flexible navigation** with Link and useRouter
- **API routes** with Route Handlers
- **Metadata management** at route level

Use the appropriate file conventions and patterns to build fast, maintainable applications.
