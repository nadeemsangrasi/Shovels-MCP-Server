# Next.js 16 Server and Client Components

This document explains the differences between Server Components and Client Components in Next.js 16, including when to use each and best practices.

## Overview

Next.js 16 is built on React Server Components, a new paradigm that allows rendering components on the server. Understanding the distinction between Server and Client Components is crucial for building performant Next.js applications.

**Default Behavior:** All components in the App Router are Server Components by default unless explicitly marked as Client Components with the `'use client'` directive.

## Server Components

### What Are Server Components?

Server Components are React components that render exclusively on the server. They:
- Run only during build time or on the server
- Have no client-side JavaScript footprint
- Can directly access server-side resources (databases, file systems, etc.)
- Support async/await for data fetching

### Basic Server Component

```typescript
// app/page.tsx
// This is a Server Component by default (no 'use client')

async function getPosts() {
  const res = await fetch('https://api.example.com/posts')
  return res.json()
}

export default async function HomePage() {
  const posts = await getPosts()

  return (
    <div>
      <h1>My Blog</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  )
}
```

### Benefits of Server Components

1. **Smaller Bundle Size**
   - No client-side JavaScript for Server Components
   - Reduced initial page load

2. **Direct Backend Access**
   ```typescript
   import { db } from '@/lib/database'

   export default async function UsersPage() {
     // Direct database access (no API route needed)
     const users = await db.user.findMany()

     return <ul>{/* Render users */}</ul>
   }
   ```

3. **Improved Security**
   - API keys and secrets stay on server
   - Sensitive logic not exposed to client

4. **Better SEO**
   - Fully rendered HTML sent to client
   - Crawlers see complete content

5. **Automatic Code Splitting**
   - Server Components don't add to bundle size

### What Server Components Can Do

✅ Fetch data directly
✅ Access backend resources (databases, file systems)
✅ Keep sensitive information on server (API keys, tokens)
✅ Keep large dependencies on server (markdown processors, etc.)
✅ Use async/await
✅ Read environment variables

```typescript
// All of these work in Server Components
import { db } from '@/lib/database'
import fs from 'fs'
import path from 'path'

export default async function ServerPage() {
  // Database access
  const users = await db.user.findMany()

  // File system access
  const filePath = path.join(process.cwd(), 'data', 'config.json')
  const fileContents = fs.readFileSync(filePath, 'utf8')

  // Environment variables
  const apiKey = process.env.API_KEY

  return <div>{/* Render data */}</div>
}
```

### What Server Components CANNOT Do

❌ Use React hooks (`useState`, `useEffect`, `useContext`, etc.)
❌ Handle browser events (`onClick`, `onChange`, etc.)
❌ Access browser APIs (`window`, `document`, `localStorage`)
❌ Use `'use client'` directive
❌ Create context providers

```typescript
// ❌ This will NOT work in Server Components
export default function ServerPage() {
  const [count, setCount] = useState(0) // Error!

  return (
    <button onClick={() => setCount(count + 1)}> // Error!
      Count: {count}
    </button>
  )
}
```

## Client Components

### What Are Client Components?

Client Components are traditional React components that:
- Render on the client (browser)
- Can use React hooks and browser APIs
- Handle interactivity and state
- Are marked with `'use client'` directive

### Basic Client Component

```typescript
// app/components/Counter.tsx
'use client' // This directive marks it as a Client Component

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  )
}
```

### When to Use Client Components

Use Client Components when you need:

1. **Interactivity and Event Listeners**
   ```typescript
   'use client'

   export function Button() {
     return <button onClick={() => alert('Clicked!')}>Click me</button>
   }
   ```

2. **State Management**
   ```typescript
   'use client'
   import { useState } from 'react'

   export function Form() {
     const [value, setValue] = useState('')
     return <input value={value} onChange={(e) => setValue(e.target.value)} />
   }
   ```

3. **Effects and Lifecycle**
   ```typescript
   'use client'
   import { useEffect } from 'react'

   export function Analytics() {
     useEffect(() => {
       trackPageView()
     }, [])

     return null
   }
   ```

4. **Browser APIs**
   ```typescript
   'use client'
   import { useEffect } from 'react'

   export function LocalStorage() {
     useEffect(() => {
       const data = localStorage.getItem('key')
     }, [])

     return <div>Data loaded</div>
   }
   ```

5. **Custom Hooks**
   ```typescript
   'use client'

   function useWindowSize() {
     const [size, setSize] = useState({ width: 0, height: 0 })

     useEffect(() => {
       const handleResize = () => {
         setSize({ width: window.innerWidth, height: window.innerHeight })
       }
       handleResize()
       window.addEventListener('resize', handleResize)
       return () => window.removeEventListener('resize', handleResize)
     }, [])

     return size
   }

   export function WindowInfo() {
     const { width, height } = useWindowSize()
     return <div>Window: {width} x {height}</div>
   }
   ```

6. **Third-Party Libraries Using React Hooks**
   ```typescript
   'use client'
   import { Carousel } from 'react-responsive-carousel'

   export function ImageGallery({ images }) {
     return <Carousel>{/* images */}</Carousel>
   }
   ```

## Composition Patterns

### Pattern 1: Server Component Wrapping Client Component

**Most common pattern** - Fetch data in Server Component, pass to Client Component:

```typescript
// app/page.tsx (Server Component)
import { Counter } from './components/Counter' // Client Component

async function getInitialCount() {
  const res = await fetch('https://api.example.com/count')
  return res.json()
}

export default async function Page() {
  const { count } = await getInitialCount()

  return (
    <div>
      <h1>Server-rendered heading</h1>
      {/* Pass server data to client component */}
      <Counter initialCount={count} />
    </div>
  )
}

// app/components/Counter.tsx (Client Component)
'use client'
import { useState } from 'react'

export function Counter({ initialCount }: { initialCount: number }) {
  const [count, setCount] = useState(initialCount)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  )
}
```

### Pattern 2: Client Component with Server Component Children

You can pass Server Components as children to Client Components:

```typescript
// app/components/ClientWrapper.tsx (Client Component)
'use client'
import { useState } from 'react'

export function ClientWrapper({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {isOpen && children}
    </div>
  )
}

// app/page.tsx (Server Component)
import { ClientWrapper } from './components/ClientWrapper'

async function ServerContent() {
  const data = await fetch('...').then(r => r.json())
  return <div>{data.content}</div>
}

export default function Page() {
  return (
    <ClientWrapper>
      {/* Server Component as child */}
      <ServerContent />
    </ClientWrapper>
  )
}
```

### Pattern 3: Keeping Client Components Small

Push Client Components down the tree for better performance:

```typescript
// ❌ Bad: Entire page is a Client Component
'use client'

export default function Page() {
  const [selected, setSelected] = useState(null)

  return (
    <div>
      <Header /> {/* Could be Server Component */}
      <StaticContent /> {/* Could be Server Component */}
      <InteractiveWidget selected={selected} onChange={setSelected} />
      <Footer /> {/* Could be Server Component */}
    </div>
  )
}

// ✅ Good: Only interactive part is Client Component
// app/page.tsx (Server Component)
import { Header } from './components/Header'
import { Footer } from './components/Footer'
import { StaticContent } from './components/StaticContent'
import { InteractiveWidget } from './components/InteractiveWidget'

export default function Page() {
  return (
    <div>
      <Header /> {/* Server Component */}
      <StaticContent /> {/* Server Component */}
      <InteractiveWidget /> {/* Client Component */}
      <Footer /> {/* Server Component */}
    </div>
  )
}

// app/components/InteractiveWidget.tsx (Client Component)
'use client'
import { useState } from 'react'

export function InteractiveWidget() {
  const [selected, setSelected] = useState(null)
  // Interactive logic here
  return <div>{/* Interactive UI */}</div>
}
```

## Handling Third-Party Libraries

### Library Using Client Features

Wrap third-party libraries that use React hooks or browser APIs:

```typescript
// app/components/CarouselWrapper.tsx
'use client'

import { Carousel } from 'acme-carousel' // Uses useState internally

export function CarouselWrapper({ images }) {
  return <Carousel>{images.map(/* ... */)}</Carousel>
}

// app/page.tsx (Server Component)
import { CarouselWrapper } from './components/CarouselWrapper'

export default async function GalleryPage() {
  const images = await fetch('...').then(r => r.json())

  return (
    <div>
      <h1>Gallery</h1>
      <CarouselWrapper images={images} />
    </div>
  )
}
```

### Context Providers

Context providers must be Client Components:

```typescript
// app/providers/ThemeProvider.tsx
'use client'

import { createContext, useContext, useState } from 'react'

const ThemeContext = createContext({
  theme: 'light',
  toggleTheme: () => {},
})

export function ThemeProvider({ children }: { children: React.ReactNode }) {
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

// app/layout.tsx (Server Component)
import { ThemeProvider } from './providers/ThemeProvider'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

## Data Fetching Strategies

### Server Component: Direct Data Access

```typescript
// app/users/page.tsx (Server Component)
import { db } from '@/lib/database'

export default async function UsersPage() {
  const users = await db.user.findMany()

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

### Client Component: Fetch on Mount

```typescript
// app/components/LiveData.tsx (Client Component)
'use client'

import { useEffect, useState } from 'react'

export function LiveData() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('/api/live-data')
      .then(r => r.json())
      .then(setData)
  }, [])

  if (!data) return <div>Loading...</div>

  return <div>{data.value}</div>
}
```

### Hybrid: Server Fetches, Client Displays

```typescript
// app/page.tsx (Server Component)
import { Dashboard } from './components/Dashboard'

async function getDashboardData() {
  const res = await fetch('https://api.example.com/dashboard')
  return res.json()
}

export default async function DashboardPage() {
  const data = await getDashboardData()

  return <Dashboard data={data} /> // Client Component
}

// app/components/Dashboard.tsx (Client Component)
'use client'

import { useState } from 'react'

export function Dashboard({ data }) {
  const [filter, setFilter] = useState('all')

  const filteredData = data.filter(/* ... */)

  return (
    <div>
      <select value={filter} onChange={e => setFilter(e.target.value)}>
        <option value="all">All</option>
        <option value="active">Active</option>
      </select>
      {filteredData.map(/* ... */)}
    </div>
  )
}
```

## Common Pitfalls

### ❌ Pitfall 1: Using Hooks in Server Components

```typescript
// ❌ Wrong
export default function Page() {
  const [state, setState] = useState(0) // Error!
  return <div>{state}</div>
}

// ✅ Correct
'use client'
export default function Page() {
  const [state, setState] = useState(0)
  return <div>{state}</div>
}
```

### ❌ Pitfall 2: Importing Server-Only Code in Client Components

```typescript
// ❌ Wrong
'use client'
import { db } from '@/lib/database' // Error! Database import in client

export function Users() {
  return <div>Users</div>
}

// ✅ Correct: Fetch data in Server Component
async function getUsers() {
  return db.user.findMany()
}

export default async function UsersPage() {
  const users = await getUsers()
  return <UsersList users={users} /> // Pass to Client Component
}
```

### ❌ Pitfall 3: Making Entire Page Client Component

```typescript
// ❌ Wrong: Unnecessarily large client bundle
'use client'

export default function Page() {
  const [tab, setTab] = useState('home')

  return (
    <div>
      <LargeStaticHeader /> {/* Could be server */}
      <LargeStaticSidebar /> {/* Could be server */}
      <TabSelector tab={tab} onTabChange={setTab} /> {/* Only this needs client */}
      <LargeStaticFooter /> {/* Could be server */}
    </div>
  )
}

// ✅ Correct: Isolate client logic
export default function Page() {
  return (
    <div>
      <LargeStaticHeader /> {/* Server Component */}
      <LargeStaticSidebar /> {/* Server Component */}
      <TabSelector /> {/* Client Component */}
      <LargeStaticFooter /> {/* Server Component */}
    </div>
  )
}
```

## Best Practices

### 1. Server Components by Default

Start with Server Components and only add `'use client'` when necessary:

```typescript
// Default to Server Components
export default async function Page() {
  const data = await fetchData()
  return <Content data={data} />
}
```

### 2. Push Client Components Down

Keep Client Components as small and deep in the tree as possible:

```typescript
// ✅ Good composition
<ServerComponent>
  <ServerComponent>
    <ServerComponent>
      <ClientComponent /> {/* Only interactive leaf */}
    </ServerComponent>
  </ServerComponent>
</ServerComponent>
```

### 3. Pass Server Data as Props

Fetch in Server Components, pass to Client Components:

```typescript
// Server Component
export default async function Page() {
  const data = await fetchData()
  return <ClientComponent data={data} />
}
```

### 4. Use 'server-only' Package

Ensure server code never leaks to client:

```typescript
// lib/database.ts
import 'server-only'

export async function getUsers() {
  // This code will throw error if imported in Client Component
  return db.user.findMany()
}
```

### 5. Serialize Props

Props passed from Server to Client Components must be serializable:

```typescript
// ❌ Wrong: Functions can't be serialized
<ClientComponent onClick={() => {}} /> // Error!

// ✅ Correct: Define function in Client Component
// Or use Server Actions for server-side functions
```

## Decision Tree

Use this to decide Server vs Client Component:

```
Does it need interactivity (clicks, input)?
  → YES: Client Component
  → NO: Continue

Does it use React hooks?
  → YES: Client Component
  → NO: Continue

Does it access browser APIs?
  → YES: Client Component
  → NO: Continue

Does it fetch data or access backend resources?
  → YES: Server Component
  → NO: Server Component (default)
```

## Performance Implications

### Server Components
- ✅ Zero client-side JavaScript
- ✅ Smaller bundle size
- ✅ Better initial load time
- ❌ Can't be interactive

### Client Components
- ✅ Full interactivity
- ✅ React hooks available
- ❌ Adds to bundle size
- ❌ Requires hydration

**Goal:** Maximize Server Components, minimize Client Components for best performance.

## Summary

| Feature | Server Component | Client Component |
|---------|------------------|------------------|
| Default | ✅ Yes | ❌ No (needs `'use client'`) |
| Data Fetching | ✅ Direct (async/await) | ⚠️ useEffect + fetch |
| Backend Access | ✅ Yes | ❌ No |
| React Hooks | ❌ No | ✅ Yes |
| Browser APIs | ❌ No | ✅ Yes |
| Event Handlers | ❌ No | ✅ Yes |
| Bundle Impact | ✅ Zero | ❌ Adds to bundle |
| When to Use | Default, data fetching | Interactivity needed |

**Remember:** Server Components are the default in Next.js 16 App Router. Only use Client Components when you need interactivity, hooks, or browser APIs.
