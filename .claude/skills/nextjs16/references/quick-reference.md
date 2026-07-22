# Next.js 16 Quick Reference

Fast reference for common Next.js 16 patterns and snippets.

## File Conventions

```
app/
├── layout.tsx          # Layout (shared UI)
├── page.tsx            # Page (route content)
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── route.ts            # API route
└── template.tsx        # Re-rendered layout
```

## Basic Page

```typescript
// Server Component (default)
export default function Page() {
  return <h1>Hello Next.js 16</h1>
}
```

## Root Layout

```typescript
// app/layout.tsx - Required!
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

## Dynamic Routes

```typescript
// app/blog/[slug]/page.tsx
export default function Post({ params }: { params: { slug: string } }) {
  return <h1>Post: {params.slug}</h1>
}

// app/shop/[...slug]/page.tsx - Catch-all
export default function Shop({ params }: { params: { slug: string[] } }) {
  return <p>Path: {params.slug.join('/')}</p>
}
```

## Data Fetching

### Static (Cached)

```typescript
const data = await fetch('https://...', {
  cache: 'force-cache' // Default
})
```

### Dynamic (No Cache)

```typescript
const data = await fetch('https://...', {
  cache: 'no-store'
})
```

### ISR (Revalidated)

```typescript
const data = await fetch('https://...', {
  next: { revalidate: 3600 } // Seconds
})
```

### Tagged (On-Demand)

```typescript
// Fetch with tag
const data = await fetch('https://...', {
  next: { tags: ['posts'] }
})

// Revalidate
import { revalidateTag } from 'next/cache'
revalidateTag('posts')
```

## Page with Data

```typescript
async function getData() {
  const res = await fetch('https://api.example.com/data')
  if (!res.ok) throw new Error('Failed')
  return res.json()
}

export default async function Page() {
  const data = await getData()
  return <div>{data.content}</div>
}
```

## Client Component

```typescript
'use client'

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

## Server + Client Composition

```typescript
// Server Component
import { ClientComponent } from './ClientComponent'

async function getData() {
  return fetch('https://...').then(r => r.json())
}

export default async function Page() {
  const data = await getData()
  return <ClientComponent data={data} />
}
```

## Server Actions

### Basic Form

```typescript
// app/actions.ts
'use server'

export async function createItem(formData: FormData) {
  const name = formData.get('name') as string
  await db.items.create({ data: { name } })
}

// app/page.tsx
import { createItem } from './actions'

export default function Page() {
  return (
    <form action={createItem}>
      <input name="name" required />
      <button type="submit">Create</button>
    </form>
  )
}
```

### With Revalidation

```typescript
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  await db.post.create({ /* ... */ })
  revalidatePath('/posts')
  redirect('/posts')
}
```

### With Loading State

```typescript
'use client'

import { useFormStatus } from 'react-dom'

function SubmitButton() {
  const { pending } = useFormStatus()
  return <button disabled={pending}>{pending ? 'Saving...' : 'Save'}</button>
}

export function Form() {
  return (
    <form action={serverAction}>
      <input name="title" />
      <SubmitButton />
    </form>
  )
}
```

### With State

```typescript
'use client'

import { useFormState } from 'react-dom'

const initialState = { message: '' }

export function Form() {
  const [state, formAction] = useFormState(serverAction, initialState)

  return (
    <form action={formAction}>
      <input name="item" />
      <button type="submit">Add</button>
      {state.message && <p>{state.message}</p>}
    </form>
  )
}
```

## Navigation

### Link

```typescript
import Link from 'next/link'

<Link href="/about">About</Link>
<Link href="/blog/hello-world">Post</Link>
<Link href={{ pathname: '/search', query: { q: 'nextjs' } }}>Search</Link>
```

### Programmatic

```typescript
'use client'

import { useRouter } from 'next/navigation'

export function Button() {
  const router = useRouter()

  return (
    <>
      <button onClick={() => router.push('/dashboard')}>Go</button>
      <button onClick={() => router.back()}>Back</button>
      <button onClick={() => router.refresh()}>Refresh</button>
    </>
  )
}
```

### Redirect (Server)

```typescript
import { redirect } from 'next/navigation'

export default async function Page() {
  const session = await getSession()
  if (!session) redirect('/login')
  return <div>Protected</div>
}
```

## Loading States

### Auto Loading

```typescript
// app/blog/loading.tsx
export default function Loading() {
  return <div>Loading...</div>
}
```

### Manual Suspense

```typescript
import { Suspense } from 'react'

async function SlowComponent() {
  const data = await fetch('...')
  return <div>{data}</div>
}

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SlowComponent />
    </Suspense>
  )
}
```

## Error Handling

### Error Boundary

```typescript
// app/blog/error.tsx
'use client'

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

### Not Found

```typescript
// app/blog/not-found.tsx
export default function NotFound() {
  return <h2>Post Not Found</h2>
}

// Trigger programmatically
import { notFound } from 'next/navigation'

export default async function Page({ params }) {
  const data = await getData(params.id)
  if (!data) notFound()
  return <div>{data.content}</div>
}
```

## Metadata

### Static

```typescript
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My Page',
  description: 'Page description',
}

export default function Page() {
  return <div>Content</div>
}
```

### Dynamic

```typescript
export async function generateMetadata({ params }) {
  const post = await getPost(params.id)

  return {
    title: post.title,
    description: post.excerpt,
  }
}

export default function Page({ params }) {
  return <article>...</article>
}
```

## Route Handlers (API)

```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const posts = await db.posts.findMany()
  return NextResponse.json(posts)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const post = await db.posts.create({ data: body })
  return NextResponse.json(post, { status: 201 })
}

// app/api/posts/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const post = await db.posts.findUnique({ where: { id: params.id } })
  if (!post) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 })
  }
  return NextResponse.json(post)
}
```

## Images

```typescript
import Image from 'next/image'

// Local image
import logo from './logo.png'
<Image src={logo} alt="Logo" />

// Remote image
<Image
  src="https://example.com/image.jpg"
  alt="Description"
  width={600}
  height={400}
  priority // For above-the-fold images
/>

// Fill container
<div style={{ position: 'relative', width: '100%', height: '400px' }}>
  <Image
    src="/hero.jpg"
    alt="Hero"
    fill
    style={{ objectFit: 'cover' }}
  />
</div>
```

## Parallel Fetching

```typescript
export default async function Page() {
  // Fetch in parallel
  const [posts, users, comments] = await Promise.all([
    fetch('https://api.example.com/posts').then(r => r.json()),
    fetch('https://api.example.com/users').then(r => r.json()),
    fetch('https://api.example.com/comments').then(r => r.json()),
  ])

  return <div>{/* Render all data */}</div>
}
```

## Sequential Fetching

```typescript
export default async function Page() {
  // First fetch
  const user = await fetch('https://...').then(r => r.json())

  // Second fetch depends on first
  const posts = await fetch(`https://...?userId=${user.id}`).then(r => r.json())

  return <div>{/* Render */}</div>
}
```

## Route Groups

```
app/
├── (marketing)/
│   ├── layout.tsx
│   ├── about/page.tsx       # /about
│   └── contact/page.tsx     # /contact
└── (shop)/
    ├── layout.tsx
    └── products/page.tsx    # /products
```

## Environment Variables

```typescript
// Server Component (safe)
const apiKey = process.env.API_KEY

// Client Component (must be prefixed with NEXT_PUBLIC_)
const publicKey = process.env.NEXT_PUBLIC_API_KEY
```

## Cookies

```typescript
// Server Component or Server Action
import { cookies } from 'next/headers'

// Read
const session = cookies().get('session')

// Set
cookies().set('session', token, {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'lax',
  maxAge: 60 * 60 * 24 * 7 // 7 days
})

// Delete
cookies().delete('session')
```

## Headers

```typescript
// Server Component or Server Action
import { headers } from 'next/headers'

const headersList = headers()
const userAgent = headersList.get('user-agent')
const referer = headersList.get('referer')
```

## Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Check auth
  const session = request.cookies.get('session')

  if (!session) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: '/dashboard/:path*'
}
```

## Context Providers

```typescript
// app/providers.tsx
'use client'

import { createContext, useContext, useState } from 'react'

const ThemeContext = createContext({ theme: 'light', toggleTheme: () => {} })

export function Providers({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState('light')

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light')
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => useContext(ThemeContext)

// app/layout.tsx
import { Providers } from './providers'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

## Common Hooks

```typescript
'use client'

import {
  useRouter,      // Programmatic navigation
  usePathname,    // Current pathname
  useSearchParams, // URL search params
  useParams,      // Route params
} from 'next/navigation'

export function Component() {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()
  const params = useParams()

  return <div>{pathname}</div>
}
```

## TypeScript Types

```typescript
import type { Metadata } from 'next'
import type { NextRequest, NextResponse } from 'next/server'

// Page Props
type PageProps = {
  params: { id: string }
  searchParams: { [key: string]: string | string[] | undefined }
}

export default function Page({ params, searchParams }: PageProps) {
  return <div>{params.id}</div>
}

// Layout Props
type LayoutProps = {
  children: React.ReactNode
  params: { id: string }
}

export default function Layout({ children, params }: LayoutProps) {
  return <div>{children}</div>
}
```

## Common Patterns Cheat Sheet

| Need | Solution |
|------|----------|
| Static page | Server Component + `cache: 'force-cache'` |
| Dynamic page | Server Component + `cache: 'no-store'` |
| Periodic updates | Server Component + `revalidate: N` |
| Interactivity | Client Component + `'use client'` |
| Form submission | Server Action + `'use server'` |
| API endpoint | Route Handler in `route.ts` |
| Loading state | `loading.tsx` or `<Suspense>` |
| Error handling | `error.tsx` |
| 404 page | `not-found.tsx` + `notFound()` |
| Protected route | Middleware or layout redirect |
| SEO metadata | `metadata` export or `generateMetadata` |
| Image optimization | `next/image` component |
| Navigation | `<Link>` or `useRouter()` |

## Decision Tree

```
Need interactivity?
├─ Yes → Client Component ('use client')
└─ No → Server Component (default)

Need data?
├─ Rarely changes → cache: 'force-cache'
├─ User-specific → cache: 'no-store'
├─ Periodic → revalidate: N
└─ Event-based → tags + revalidateTag()

Need to mutate data?
├─ From form → Server Action
└─ From JS → Server Action or Route Handler
```

This quick reference covers 90% of common Next.js 16 use cases. For detailed explanations, see the full documentation in `references/official-docs/`.
