# Next.js 16 Data Fetching Guide

This document contains official Next.js 16 data fetching patterns and best practices fetched from Context7.

## Overview

Next.js 16 extends the native Web `fetch()` API to provide powerful caching and revalidation capabilities. Server Components can fetch data directly using async/await, eliminating the need for separate API routes in many cases.

## Basic Data Fetching in Server Components

### Simple Fetch Example

```typescript
export default async function Page() {
  const data = await fetch('https://api.vercel.app/blog')
  const posts = await data.json()

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

**Key Points:**
- Server Components are async by default
- Data is fetched on the server
- No client-side JavaScript needed for static data
- Results are automatically cached

## Caching Strategies

### 1. Static Data Fetching (Force Cache)

**Use for:** Data that rarely changes, build-time content

```typescript
export default async function Page() {
  // This request is cached until manually invalidated
  // Similar to getStaticProps from Pages Router
  const staticData = await fetch('https://api.example.com/data', {
    cache: 'force-cache' // This is the default and can be omitted
  })

  const data = await staticData.json()
  return <div>{data.content}</div>
}
```

**Behavior:**
- Data fetched at build time
- Cached indefinitely
- Reused across requests
- Best for performance

### 2. Dynamic Data Fetching (No Store)

**Use for:** Real-time data, user-specific content, frequently changing data

```typescript
export default async function Page() {
  // This request is refetched on every request
  // Similar to getServerSideProps from Pages Router
  const dynamicData = await fetch('https://api.example.com/stats', {
    cache: 'no-store'
  })

  const stats = await dynamicData.json()
  return <div>Current stats: {stats.value}</div>
}
```

**Behavior:**
- Data fetched on every request
- Always fresh
- No caching
- Higher server load

### 3. Revalidated Data Fetching (ISR)

**Use for:** Data that changes periodically (products, blog posts with comments)

```typescript
export default async function Page() {
  // Cache with a lifetime of 10 seconds
  // Similar to getStaticProps with revalidate option
  const revalidatedData = await fetch('https://api.example.com/products', {
    next: { revalidate: 10 }
  })

  const products = await revalidatedData.json()
  return <div>{/* Render products */}</div>
}
```

**Behavior:**
- Data cached for specified duration (in seconds)
- Automatically revalidates after TTL expires
- Balance between freshness and performance

### 4. Tag-Based Revalidation

**Use for:** On-demand revalidation triggered by events (new post published, product updated)

```typescript
// Fetching with tags
export default async function PostsPage() {
  const res = await fetch('https://api.example.com/posts', {
    next: { tags: ['posts'] }
  })

  const posts = await res.json()
  return <ul>{/* Render posts */}</ul>
}

// Revalidating from a Server Action
'use server'

import { revalidateTag } from 'next/cache'

export async function publishPost() {
  // Invalidate all requests tagged with 'posts'
  revalidateTag('posts')
}

// Revalidating from a Route Handler
import { revalidateTag } from 'next/cache'

export async function POST() {
  revalidateTag('posts')
  return Response.json({ revalidated: true })
}
```

**Behavior:**
- Cache invalidated on-demand
- All requests with same tag revalidated
- Precise cache control

## Advanced Patterns

### Parallel Data Fetching

```typescript
async function getUser(id: string) {
  const res = await fetch(`https://api.example.com/users/${id}`)
  return res.json()
}

async function getPosts(userId: string) {
  const res = await fetch(`https://api.example.com/posts?userId=${userId}`)
  return res.json()
}

export default async function ProfilePage({ params }: { params: { id: string } }) {
  // Fetch in parallel using Promise.all
  const [user, posts] = await Promise.all([
    getUser(params.id),
    getPosts(params.id)
  ])

  return (
    <div>
      <h1>{user.name}</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  )
}
```

### Sequential Data Fetching

```typescript
export default async function Page() {
  // First fetch
  const user = await fetch('https://api.example.com/user').then(r => r.json())

  // Second fetch depends on first
  const preferences = await fetch(
    `https://api.example.com/preferences?userId=${user.id}`
  ).then(r => r.json())

  return <div>{/* Render with both */}</div>
}
```

### Streaming with Suspense

```typescript
import { Suspense } from 'react'

async function Posts() {
  const res = await fetch('https://api.example.com/posts', {
    cache: 'no-store'
  })
  const posts = await res.json()

  return <ul>{/* Render posts */}</ul>
}

export default function Page() {
  return (
    <div>
      <h1>My Blog</h1>
      <Suspense fallback={<div>Loading posts...</div>}>
        <Posts />
      </Suspense>
    </div>
  )
}
```

## Passing Data Between Components

### Server Component to Client Component

```typescript
// Server Component (page.tsx)
import HomePage from './home-page' // Client Component

async function getPosts() {
  const res = await fetch('https://api.example.com/posts')
  return res.json()
}

export default async function Page() {
  const posts = await getPosts()

  // Pass data as props to Client Component
  return <HomePage posts={posts} />
}

// Client Component (home-page.tsx)
'use client'

export default function HomePage({ posts }: { posts: Post[] }) {
  // Use the data with client-side interactivity
  return (
    <div>
      {posts.map(post => (
        <article key={post.id} onClick={() => handleClick(post)}>
          {post.title}
        </article>
      ))}
    </div>
  )
}
```

## Request Deduplication

Next.js automatically deduplicates identical fetch requests within the same render pass:

```typescript
async function getData() {
  const res = await fetch('https://api.example.com/data')
  return res.json()
}

export default async function Page() {
  // Even if called multiple times, only one request is made
  return (
    <>
      <ComponentOne /> {/* Calls getData() */}
      <ComponentTwo /> {/* Calls getData() - deduped! */}
    </>
  )
}
```

## Error Handling

### Try-Catch Pattern

```typescript
async function getData() {
  try {
    const res = await fetch('https://api.example.com/data')

    if (!res.ok) {
      throw new Error('Failed to fetch data')
    }

    return res.json()
  } catch (error) {
    console.error('Fetch error:', error)
    throw error // Re-throw to trigger error boundary
  }
}

export default async function Page() {
  const data = await getData()
  return <div>{data.content}</div>
}
```

### With Error Boundary

```typescript
// error.tsx
'use client'

export default function Error({ error, reset }: {
  error: Error
  reset: () => void
}) {
  return (
    <div>
      <h2>Failed to load data</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

## Best Practices

### 1. Choose the Right Caching Strategy

```typescript
// Static content (blog posts, documentation)
const posts = await fetch('...', { cache: 'force-cache' })

// User-specific data (dashboards, profiles)
const userData = await fetch('...', { cache: 'no-store' })

// Product listings (balance freshness and performance)
const products = await fetch('...', { next: { revalidate: 3600 } })

// CMS content (revalidate on publish)
const content = await fetch('...', { next: { tags: ['content'] } })
```

### 2. Handle Loading States

Use `loading.tsx` for automatic loading UI:

```typescript
// app/posts/loading.tsx
export default function Loading() {
  return <div>Loading posts...</div>
}

// app/posts/page.tsx
export default async function PostsPage() {
  const posts = await fetch('...').then(r => r.json())
  return <ul>{/* posts */}</ul>
}
```

### 3. Validate Data

```typescript
import { z } from 'zod'

const PostSchema = z.object({
  id: z.string(),
  title: z.string(),
  content: z.string()
})

async function getPosts() {
  const res = await fetch('https://api.example.com/posts')
  const data = await res.json()

  // Validate data structure
  return z.array(PostSchema).parse(data)
}
```

### 4. Use TypeScript

```typescript
interface Post {
  id: string
  title: string
  content: string
  publishedAt: string
}

async function getPosts(): Promise<Post[]> {
  const res = await fetch('https://api.example.com/posts')
  return res.json()
}

export default async function PostsPage() {
  const posts: Post[] = await getPosts()
  return <div>{/* Type-safe rendering */}</div>
}
```

## Performance Tips

1. **Use appropriate cache strategies** - Don't use `no-store` unless necessary
2. **Fetch in parallel** when possible - Use `Promise.all()`
3. **Colocate data fetching** - Fetch data close to where it's used
4. **Use Suspense boundaries** - Stream content as it becomes available
5. **Implement loading states** - Improve perceived performance
6. **Monitor cache hit rates** - Optimize revalidation timings

## Common Pitfalls

### ❌ Fetching in Client Components

```typescript
'use client'

export default function Posts() {
  const [posts, setPosts] = useState([])

  useEffect(() => {
    fetch('https://api.example.com/posts')
      .then(r => r.json())
      .then(setPosts)
  }, [])

  return <ul>{/* posts */}</ul>
}
```

### ✅ Fetch in Server Component, Pass to Client

```typescript
// Server Component
async function getPosts() {
  return fetch('https://api.example.com/posts').then(r => r.json())
}

export default async function Page() {
  const posts = await getPosts()
  return <PostsList posts={posts} /> // Client Component
}
```

## Migration from Pages Router

### getStaticProps → Server Component with force-cache

```typescript
// Before (Pages Router)
export async function getStaticProps() {
  const res = await fetch('https://api.example.com/posts')
  const posts = await res.json()
  return { props: { posts } }
}

// After (App Router)
export default async function Page() {
  const res = await fetch('https://api.example.com/posts', {
    cache: 'force-cache'
  })
  const posts = await res.json()
  return <div>{/* posts */}</div>
}
```

### getServerSideProps → Server Component with no-store

```typescript
// Before (Pages Router)
export async function getServerSideProps() {
  const res = await fetch('https://api.example.com/data')
  const data = await res.json()
  return { props: { data } }
}

// After (App Router)
export default async function Page() {
  const res = await fetch('https://api.example.com/data', {
    cache: 'no-store'
  })
  const data = await res.json()
  return <div>{data.content}</div>
}
```

## Summary

Next.js 16 provides powerful data fetching capabilities:
- **Server Components** fetch data directly with async/await
- **Multiple caching strategies** for different use cases
- **Automatic request deduplication** for efficiency
- **Tag-based revalidation** for precise cache control
- **Seamless integration** with loading and error states

Choose the right strategy based on your data's characteristics and update frequency.
