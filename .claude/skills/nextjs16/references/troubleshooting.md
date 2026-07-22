# Next.js 16 Troubleshooting Guide

Common errors, solutions, and debugging tips for Next.js 16 applications.

## Common Errors

### 1. "You're importing a component that needs useState..."

**Error:**
```
Error: You're importing a component that needs useState.
It only works in a Client Component but none of its parents are marked with "use client"
```

**Cause:** Using React hooks in a Server Component

**Solution:**
```typescript
// ❌ Wrong - Server Component using hooks
export default function Page() {
  const [state, setState] = useState(0) // Error!
  return <div>{state}</div>
}

// ✅ Correct - Add 'use client' directive
'use client'

export default function Page() {
  const [state, setState] = useState(0)
  return <div>{state}</div>
}
```

---

### 2. "fetch failed" / Network Errors

**Error:**
```
Error: fetch failed
TypeError: fetch failed
```

**Common Causes & Solutions:**

**A. API endpoint doesn't exist:**
```typescript
// Check the URL is correct
const res = await fetch('https://api.example.com/posts')
console.log(res.status) // Check status code
```

**B. Missing error handling:**
```typescript
// ❌ Wrong - No error handling
const res = await fetch('https://...')
const data = await res.json()

// ✅ Correct - With error handling
try {
  const res = await fetch('https://...')

  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`)
  }

  const data = await res.json()
  return data
} catch (error) {
  console.error('Fetch error:', error)
  throw error // Re-throw to trigger error boundary
}
```

**C. CORS issues (in development):**
```typescript
// Add headers for CORS
const res = await fetch('https://api.example.com/data', {
  headers: {
    'Content-Type': 'application/json',
  }
})

// Or use a proxy in next.config.js
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://external-api.com/:path*',
      },
    ]
  },
}
```

---

### 3. "Route not found" / 404 Errors

**Error:**
Page returns 404 even though file exists

**Causes & Solutions:**

**A. Wrong file name:**
```
❌ app/about.tsx          # Wrong - not in a folder
❌ app/about/Page.tsx     # Wrong - capital P
✅ app/about/page.tsx     # Correct - lowercase 'page'
```

**B. Missing page.tsx:**
```
❌ app/blog/[slug]/       # Folder exists but no page.tsx
✅ app/blog/[slug]/page.tsx
```

**C. Server needs restart:**
```bash
# Stop dev server (Ctrl+C)
# Clear cache
rm -rf .next

# Restart
npm run dev
```

---

### 4. "createContext is not a function"

**Error:**
```
Error: createContext is not a function
```

**Cause:** Using React Context in Server Component

**Solution:**
```typescript
// ❌ Wrong - Context in Server Component
export const ThemeContext = createContext() // Error!

export default function Layout({ children }) {
  return (
    <ThemeContext.Provider value="light">
      {children}
    </ThemeContext.Provider>
  )
}

// ✅ Correct - Move to Client Component
// app/providers.tsx
'use client'

import { createContext, useContext } from 'react'

export const ThemeContext = createContext('light')

export function Providers({ children }) {
  return (
    <ThemeContext.Provider value="light">
      {children}
    </ThemeContext.Provider>
  )
}

// app/layout.tsx (Server Component)
import { Providers } from './providers'

export default function Layout({ children }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

---

### 5. "Error: Cannot read properties of undefined"

**Error when accessing params or searchParams**

**Cause:** Params not passed correctly or accessed before ready

**Solution:**
```typescript
// ❌ Wrong - Accessing params incorrectly
export default function Page({ params }) {
  return <h1>{params.slug}</h1> // params might be undefined
}

// ✅ Correct - Type and check params
export default function Page({ params }: { params: { slug: string } }) {
  if (!params?.slug) {
    return <div>No slug provided</div>
  }

  return <h1>{params.slug}</h1>
}

// ✅ Better - Use TypeScript
type PageProps = {
  params: { slug: string }
  searchParams: { [key: string]: string | undefined }
}

export default function Page({ params, searchParams }: PageProps) {
  return <h1>{params.slug}</h1>
}
```

---

### 6. "Module not found" Errors

**Error:**
```
Module not found: Can't resolve '@/components/Button'
```

**Solutions:**

**A. Check import path:**
```typescript
// ❌ Wrong paths
import { Button } from '@/Components/Button' // Wrong case
import { Button } from 'components/Button'   // Missing @

// ✅ Correct
import { Button } from '@/components/Button'
```

**B. Check tsconfig.json paths:**
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

**C. Restart TypeScript server (in VS Code):**
```
Cmd+Shift+P → TypeScript: Restart TS Server
```

---

### 7. "Server Action must be marked with 'use server'"

**Error:**
```
Error: Functions cannot be passed directly to Client Components
```

**Cause:** Server Action not marked or passed incorrectly

**Solution:**
```typescript
// ❌ Wrong - Not marked as Server Action
export async function createPost(formData: FormData) {
  await db.post.create({ data: { /* ... */ } })
}

// ✅ Correct - Mark with 'use server'
'use server'

export async function createPost(formData: FormData) {
  await db.post.create({ data: { /* ... */ } })
}

// ✅ Or inline in Server Component
export default function Page() {
  async function handleSubmit(formData: FormData) {
    'use server'
    // Server Action code
  }

  return <form action={handleSubmit}>...</form>
}
```

---

### 8. Hydration Mismatch Errors

**Error:**
```
Warning: Text content does not match server-rendered HTML
Hydration failed because the initial UI does not match what was rendered on the server
```

**Causes & Solutions:**

**A. Using browser APIs in Server Components:**
```typescript
// ❌ Wrong - window in Server Component
export default function Page() {
  const width = window.innerWidth // Error!
  return <div>{width}</div>
}

// ✅ Correct - Use in Client Component with useEffect
'use client'

import { useEffect, useState } from 'react'

export default function Page() {
  const [width, setWidth] = useState(0)

  useEffect(() => {
    setWidth(window.innerWidth)
  }, [])

  return <div>{width}</div>
}
```

**B. Random values or dates without consistency:**
```typescript
// ❌ Wrong - Random value causes mismatch
export default function Page() {
  return <div>{Math.random()}</div>
}

// ✅ Correct - Generate on server, pass to client
export default async function Page() {
  const randomValue = Math.random()
  return <ClientComponent value={randomValue} />
}
```

**C. Conditional rendering based on browser state:**
```typescript
// ❌ Wrong - Different on server and client
export default function Page() {
  const isMobile = window.innerWidth < 768 // Server doesn't have window
  return isMobile ? <MobileView /> : <DesktopView />
}

// ✅ Correct - Use CSS or client-side only
'use client'

import { useState, useEffect } from 'react'

export default function Page() {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    setIsMobile(window.innerWidth < 768)
  }, [])

  if (!isMobile) return <DesktopView />
  return <MobileView />
}
```

---

### 9. "Error: Invariant: cookies() expects to have requestAsyncStorage..."

**Error when using cookies() outside of request context**

**Cause:** Using `cookies()` in wrong location

**Solution:**
```typescript
// ❌ Wrong - cookies() at module level
import { cookies } from 'next/headers'

const session = cookies().get('session') // Error!

export default function Page() {
  return <div>{session}</div>
}

// ✅ Correct - Inside async Server Component or Server Action
import { cookies } from 'next/headers'

export default async function Page() {
  const session = cookies().get('session')
  return <div>{session?.value}</div>
}

// ✅ Or in Server Action
'use server'

export async function getSession() {
  const session = cookies().get('session')
  return session?.value
}
```

---

### 10. Slow Page Loads / Performance Issues

**Symptoms:** Pages take long to load, slow navigation

**Solutions:**

**A. Check data fetching strategy:**
```typescript
// ❌ Wrong - Always dynamic when should be static
const data = await fetch('https://...', { cache: 'no-store' })

// ✅ Correct - Use appropriate caching
const data = await fetch('https://...', {
  cache: 'force-cache', // or revalidate: 3600
})
```

**B. Use parallel fetching:**
```typescript
// ❌ Wrong - Sequential fetching
const posts = await getPosts()
const users = await getUsers()
const comments = await getComments()

// ✅ Correct - Parallel fetching
const [posts, users, comments] = await Promise.all([
  getPosts(),
  getUsers(),
  getComments()
])
```

**C. Use Suspense for streaming:**
```typescript
import { Suspense } from 'react'

export default function Page() {
  return (
    <div>
      <FastComponent />

      <Suspense fallback={<div>Loading...</div>}>
        <SlowComponent />
      </Suspense>
    </div>
  )
}
```

**D. Optimize images:**
```typescript
// ❌ Wrong - Regular img tag
<img src="/large-image.jpg" />

// ✅ Correct - next/image with optimization
import Image from 'next/image'

<Image
  src="/large-image.jpg"
  alt="Description"
  width={800}
  height={600}
  priority // For above-the-fold images
/>
```

---

## Debugging Tips

### 1. Check Component Type

```typescript
// Add console.log to see where code runs
export default function Component() {
  console.log('Running on:', typeof window === 'undefined' ? 'server' : 'client')
  return <div>Component</div>
}
```

### 2. Inspect Fetch Requests

```typescript
async function getData() {
  console.log('Fetching data...')
  const res = await fetch('https://...')
  console.log('Status:', res.status)
  console.log('Headers:', res.headers)

  const data = await res.json()
  console.log('Data:', data)

  return data
}
```

### 3. Use React DevTools

Install React DevTools browser extension:
- View component tree
- Inspect props and state
- Check which components are Client vs Server

### 4. Check Network Tab

Open browser DevTools → Network tab:
- See all requests
- Check response status codes
- Inspect response data
- Check caching headers

### 5. Clear Next.js Cache

```bash
# Clear build cache
rm -rf .next

# Clear npm cache (if needed)
npm cache clean --force

# Restart dev server
npm run dev
```

### 6. Enable Verbose Logging

```bash
# Run with debug mode
NODE_OPTIONS='--inspect' npm run dev

# Or with verbose logging
DEBUG=* npm run dev
```

### 7. Check File Names

Common mistakes:
- `Page.tsx` → should be `page.tsx` (lowercase)
- `Layout.tsx` → should be `layout.tsx` (lowercase)
- `loading.tsx` not `Loading.tsx`
- `error.tsx` not `Error.tsx`

### 8. Verify Route Structure

```bash
# List all files in app directory
tree app/

# Or
find app -type f
```

### 9. TypeScript Errors

```bash
# Check TypeScript errors
npx tsc --noEmit

# Or use VS Code Problems panel
```

### 10. Production Build Test

```bash
# Build for production to catch build-time errors
npm run build

# Run production build locally
npm run start
```

---

## Common Gotchas

### 1. Server Components Can't Use Hooks

```typescript
// ❌ Server Component with hooks
export default function Page() {
  const [state, setState] = useState(0) // Error!
  useEffect(() => {}, []) // Error!
  return <div>{state}</div>
}

// ✅ Move to Client Component
'use client'
export default function Page() {
  const [state, setState] = useState(0)
  useEffect(() => {}, [])
  return <div>{state}</div>
}
```

### 2. Props Must Be Serializable

```typescript
// ❌ Can't pass functions from Server to Client
<ClientComponent onClick={() => {}} /> // Error!

// ✅ Use Server Actions instead
<ClientComponent action={serverAction} />
```

### 3. Layouts Don't Re-render

```typescript
// Layouts persist across navigation
// Don't put navigation-dependent state in layouts
// Use templates if you need re-rendering
```

### 4. Dynamic Routes Need Correct Syntax

```typescript
// ❌ Wrong
app/blog/:slug/page.tsx

// ✅ Correct
app/blog/[slug]/page.tsx

// ❌ Wrong
app/blog/{slug}/page.tsx

// ✅ Correct
app/blog/[slug]/page.tsx
```

### 5. Async Client Components Not Supported

```typescript
// ❌ Wrong - Client Components can't be async
'use client'

export default async function Page() { // Error!
  const data = await fetch('...')
  return <div>{data}</div>
}

// ✅ Correct - Fetch in Server Component, pass to Client
// Or use useEffect in Client Component
'use client'

import { useEffect, useState } from 'react'

export default function Page() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('...').then(r => r.json()).then(setData)
  }, [])

  return <div>{data}</div>
}
```

---

## Getting Help

### 1. Check Official Docs
- https://nextjs.org/docs

### 2. Search GitHub Issues
- https://github.com/vercel/next.js/issues

### 3. Ask on Discord
- https://nextjs.org/discord

### 4. Stack Overflow
- Tag: `next.js` + `next.js-16` + `app-router`

### 5. Use Context7 MCP
```
Query: /vercel/next.js/v16.1.0
Topic: [your specific issue]
```

---

## Preventive Checklist

Before deploying:

- [ ] All pages have proper error boundaries
- [ ] Loading states implemented
- [ ] Data fetching uses appropriate caching
- [ ] Images use next/image component
- [ ] TypeScript errors resolved
- [ ] Build passes: `npm run build`
- [ ] No console errors in browser
- [ ] Test on slow network (throttle in DevTools)
- [ ] Check mobile responsiveness
- [ ] Verify all links work
- [ ] Test form submissions
- [ ] Check 404 page works

This guide covers most common issues. For specific errors, use Context7 to query official Next.js documentation.
