# Next.js 16 Complete Examples

This document contains complete, production-ready examples for common Next.js 16 application patterns.

## Table of Contents

1. [Static Blog](#static-blog)
2. [Real-Time Dashboard](#real-time-dashboard)
3. [E-commerce Site](#e-commerce-site)
4. [Authentication System](#authentication-system)

---

## Static Blog

A blog with static generation, dynamic routes, and markdown content.

### Project Structure

```
app/
├── layout.tsx
├── page.tsx              # Home page with post list
├── blog/
│   ├── page.tsx          # Blog list
│   └── [slug]/
│       └── page.tsx      # Individual post
└── about/
    └── page.tsx
```

### Implementation

**Home Page with Post List:**

```typescript
// app/page.tsx
import Link from 'next/link'

async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    cache: 'force-cache' // Static generation
  })

  if (!res.ok) throw new Error('Failed to fetch posts')
  return res.json()
}

export default async function HomePage() {
  const posts = await getPosts()

  return (
    <div>
      <h1>My Blog</h1>
      <p>Welcome to my Next.js 16 blog</p>

      <section>
        <h2>Recent Posts</h2>
        <ul>
          {posts.slice(0, 5).map((post: any) => (
            <li key={post.id}>
              <Link href={`/blog/${post.slug}`}>
                <h3>{post.title}</h3>
                <p>{post.excerpt}</p>
                <time>{new Date(post.publishedAt).toLocaleDateString()}</time>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}
```

**Blog List Page:**

```typescript
// app/blog/page.tsx
import Link from 'next/link'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Blog Posts',
  description: 'All blog posts',
}

async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    cache: 'force-cache'
  })
  return res.json()
}

export default async function BlogPage() {
  const posts = await getPosts()

  return (
    <div>
      <h1>All Blog Posts</h1>
      <div className="post-grid">
        {posts.map((post: any) => (
          <article key={post.id}>
            <Link href={`/blog/${post.slug}`}>
              <h2>{post.title}</h2>
              <p>{post.excerpt}</p>
              <time>{new Date(post.publishedAt).toLocaleDateString()}</time>
            </Link>
          </article>
        ))}
      </div>
    </div>
  )
}
```

**Individual Post Page:**

```typescript
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation'
import { Metadata } from 'next'

async function getPost(slug: string) {
  const res = await fetch(`https://api.example.com/posts/${slug}`, {
    cache: 'force-cache'
  })

  if (!res.ok) return null
  return res.json()
}

export async function generateMetadata({ params }: {
  params: { slug: string }
}): Promise<Metadata> {
  const post = await getPost(params.slug)

  if (!post) return { title: 'Post Not Found' }

  return {
    title: post.title,
    description: post.excerpt,
  }
}

export default async function PostPage({ params }: {
  params: { slug: string }
}) {
  const post = await getPost(params.slug)

  if (!post) {
    notFound()
  }

  return (
    <article>
      <header>
        <h1>{post.title}</h1>
        <time>{new Date(post.publishedAt).toLocaleDateString()}</time>
        <p>By {post.author}</p>
      </header>

      <div
        className="prose"
        dangerouslySetInnerHTML={{ __html: post.content }}
      />

      <footer>
        <Link href="/blog">← Back to all posts</Link>
      </footer>
    </article>
  )
}

// Optional: Generate static paths at build time
export async function generateStaticParams() {
  const res = await fetch('https://api.example.com/posts')
  const posts = await res.json()

  return posts.map((post: any) => ({
    slug: post.slug,
  }))
}
```

**Not Found Page:**

```typescript
// app/blog/[slug]/not-found.tsx
import Link from 'next/link'

export default function NotFound() {
  return (
    <div>
      <h2>Post Not Found</h2>
      <p>The blog post you're looking for doesn't exist.</p>
      <Link href="/blog">View all posts</Link>
    </div>
  )
}
```

---

## Real-Time Dashboard

Dashboard with live data updates, charts, and interactive components.

### Project Structure

```
app/
├── dashboard/
│   ├── layout.tsx        # Dashboard layout with sidebar
│   ├── page.tsx          # Overview
│   ├── analytics/
│   │   └── page.tsx
│   └── settings/
│       └── page.tsx
└── components/
    ├── StatsCard.tsx     # Server Component
    └── Chart.tsx         # Client Component
```

### Implementation

**Dashboard Layout:**

```typescript
// app/dashboard/layout.tsx
import Link from 'next/link'
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

async function getUser() {
  const session = cookies().get('session')
  if (!session) return null

  // Verify session and get user
  const res = await fetch('https://api.example.com/user', {
    headers: { 'Cookie': `session=${session.value}` }
  })

  if (!res.ok) return null
  return res.json()
}

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const user = await getUser()

  if (!user) {
    redirect('/login')
  }

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>Dashboard</h2>
        <nav>
          <Link href="/dashboard">Overview</Link>
          <Link href="/dashboard/analytics">Analytics</Link>
          <Link href="/dashboard/settings">Settings</Link>
        </nav>
        <div className="user-info">
          <p>{user.name}</p>
          <p>{user.email}</p>
        </div>
      </aside>

      <main className="content">
        {children}
      </main>
    </div>
  )
}
```

**Dashboard Overview:**

```typescript
// app/dashboard/page.tsx
import { StatsCard } from '@/components/StatsCard'
import { Chart } from '@/components/Chart'

async function getStats() {
  const res = await fetch('https://api.example.com/stats', {
    cache: 'no-store' // Always fetch fresh data
  })
  return res.json()
}

async function getChartData() {
  const res = await fetch('https://api.example.com/chart-data', {
    cache: 'no-store'
  })
  return res.json()
}

export default async function DashboardPage() {
  // Fetch in parallel
  const [stats, chartData] = await Promise.all([
    getStats(),
    getChartData()
  ])

  return (
    <div>
      <h1>Dashboard Overview</h1>

      <div className="stats-grid">
        <StatsCard title="Total Users" value={stats.users} trend="+12%" />
        <StatsCard title="Revenue" value={`$${stats.revenue}`} trend="+8%" />
        <StatsCard title="Orders" value={stats.orders} trend="+23%" />
        <StatsCard title="Active Sessions" value={stats.sessions} trend="+5%" />
      </div>

      <section>
        <h2>Analytics</h2>
        {/* Client Component for interactivity */}
        <Chart data={chartData} />
      </section>
    </div>
  )
}
```

**Stats Card (Server Component):**

```typescript
// components/StatsCard.tsx
export function StatsCard({
  title,
  value,
  trend,
}: {
  title: string
  value: string | number
  trend: string
}) {
  const isPositive = trend.startsWith('+')

  return (
    <div className="stats-card">
      <h3>{title}</h3>
      <p className="value">{value}</p>
      <p className={`trend ${isPositive ? 'positive' : 'negative'}`}>
        {trend}
      </p>
    </div>
  )
}
```

**Interactive Chart (Client Component):**

```typescript
// components/Chart.tsx
'use client'

import { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts'

export function Chart({ data }: { data: any[] }) {
  const [timeRange, setTimeRange] = useState('7d')

  const filteredData = data.filter(/* filter by timeRange */)

  return (
    <div>
      <div className="controls">
        <button onClick={() => setTimeRange('7d')}>7 Days</button>
        <button onClick={() => setTimeRange('30d')}>30 Days</button>
        <button onClick={() => setTimeRange('90d')}>90 Days</button>
      </div>

      <LineChart width={600} height={300} data={filteredData}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="#8884d8" />
      </LineChart>
    </div>
  )
}
```

**Loading State:**

```typescript
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div>
      <div className="skeleton-header" />
      <div className="stats-grid">
        <div className="skeleton-card" />
        <div className="skeleton-card" />
        <div className="skeleton-card" />
        <div className="skeleton-card" />
      </div>
      <div className="skeleton-chart" />
    </div>
  )
}
```

---

## E-commerce Site

Product catalog with ISR, shopping cart, and checkout.

### Project Structure

```
app/
├── page.tsx                    # Home page
├── products/
│   ├── page.tsx               # Product list
│   └── [id]/
│       └── page.tsx           # Product detail
├── cart/
│   └── page.tsx               # Shopping cart
└── checkout/
    └── page.tsx               # Checkout
```

### Implementation

**Product List with ISR:**

```typescript
// app/products/page.tsx
import Link from 'next/link'
import Image from 'next/image'

async function getProducts() {
  const res = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 } // Revalidate every hour
  })
  return res.json()
}

export default async function ProductsPage() {
  const products = await getProducts()

  return (
    <div>
      <h1>Products</h1>

      <div className="product-grid">
        {products.map((product: any) => (
          <Link href={`/products/${product.id}`} key={product.id}>
            <article className="product-card">
              <Image
                src={product.image}
                alt={product.name}
                width={300}
                height={300}
              />
              <h2>{product.name}</h2>
              <p>${product.price}</p>
            </article>
          </Link>
        ))}
      </div>
    </div>
  )
}
```

**Product Detail with Add to Cart:**

```typescript
// app/products/[id]/page.tsx
import { notFound } from 'next/navigation'
import Image from 'next/image'
import { AddToCartButton } from '@/components/AddToCartButton'

async function getProduct(id: string) {
  const res = await fetch(`https://api.example.com/products/${id}`, {
    next: { revalidate: 3600 }
  })

  if (!res.ok) return null
  return res.json()
}

export default async function ProductPage({ params }: {
  params: { id: string }
}) {
  const product = await getProduct(params.id)

  if (!product) {
    notFound()
  }

  return (
    <div className="product-detail">
      <Image
        src={product.image}
        alt={product.name}
        width={600}
        height={600}
        priority
      />

      <div className="product-info">
        <h1>{product.name}</h1>
        <p className="price">${product.price}</p>
        <p className="description">{product.description}</p>

        <AddToCartButton product={product} />

        <div className="details">
          <h3>Product Details</h3>
          <ul>
            <li>SKU: {product.sku}</li>
            <li>Stock: {product.stock} available</li>
            <li>Category: {product.category}</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
```

**Add to Cart Button (Client Component):**

```typescript
// components/AddToCartButton.tsx
'use client'

import { useState } from 'react'
import { addToCart } from '@/app/actions/cart'

export function AddToCartButton({ product }: { product: any }) {
  const [quantity, setQuantity] = useState(1)
  const [isAdding, setIsAdding] = useState(false)

  const handleAddToCart = async () => {
    setIsAdding(true)
    try {
      await addToCart(product.id, quantity)
      alert('Added to cart!')
    } catch (error) {
      alert('Failed to add to cart')
    } finally {
      setIsAdding(false)
    }
  }

  return (
    <div className="add-to-cart">
      <div className="quantity-selector">
        <button onClick={() => setQuantity(Math.max(1, quantity - 1))}>-</button>
        <span>{quantity}</span>
        <button onClick={() => setQuantity(quantity + 1)}>+</button>
      </div>

      <button
        onClick={handleAddToCart}
        disabled={isAdding}
        className="add-to-cart-btn"
      >
        {isAdding ? 'Adding...' : 'Add to Cart'}
      </button>
    </div>
  )
}
```

**Shopping Cart Server Action:**

```typescript
// app/actions/cart.ts
'use server'

import { cookies } from 'next/headers'
import { revalidatePath } from 'next/cache'

export async function addToCart(productId: string, quantity: number) {
  const session = cookies().get('session')

  const res = await fetch('https://api.example.com/cart', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Cookie': `session=${session?.value}`
    },
    body: JSON.stringify({ productId, quantity })
  })

  if (!res.ok) {
    throw new Error('Failed to add to cart')
  }

  revalidatePath('/cart')
  return res.json()
}

export async function removeFromCart(itemId: string) {
  const session = cookies().get('session')

  await fetch(`https://api.example.com/cart/${itemId}`, {
    method: 'DELETE',
    headers: {
      'Cookie': `session=${session?.value}`
    }
  })

  revalidatePath('/cart')
}
```

**Cart Page:**

```typescript
// app/cart/page.tsx
import Link from 'next/link'
import { RemoveButton } from '@/components/RemoveButton'

async function getCart() {
  const session = cookies().get('session')

  const res = await fetch('https://api.example.com/cart', {
    headers: { 'Cookie': `session=${session?.value}` },
    cache: 'no-store'
  })

  return res.json()
}

export default async function CartPage() {
  const cart = await getCart()

  if (cart.items.length === 0) {
    return (
      <div>
        <h1>Your Cart</h1>
        <p>Your cart is empty</p>
        <Link href="/products">Continue Shopping</Link>
      </div>
    )
  }

  const total = cart.items.reduce((sum: number, item: any) =>
    sum + item.price * item.quantity, 0
  )

  return (
    <div>
      <h1>Your Cart</h1>

      <div className="cart-items">
        {cart.items.map((item: any) => (
          <div key={item.id} className="cart-item">
            <Image src={item.image} alt={item.name} width={100} height={100} />
            <div>
              <h3>{item.name}</h3>
              <p>${item.price} x {item.quantity}</p>
            </div>
            <RemoveButton itemId={item.id} />
          </div>
        ))}
      </div>

      <div className="cart-summary">
        <p>Total: ${total.toFixed(2)}</p>
        <Link href="/checkout">
          <button>Proceed to Checkout</button>
        </Link>
      </div>
    </div>
  )
}
```

---

## Authentication System

Complete authentication with signup, login, and protected routes.

### Implementation

**Signup/Login Actions:**

```typescript
// app/actions/auth.ts
'use server'

import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import bcrypt from 'bcryptjs'

export async function signup(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string
  const password = formData.get('password') as string

  // Validate
  if (!name || !email || !password) {
    return { error: 'All fields required' }
  }

  // Hash password
  const hashedPassword = await bcrypt.hash(password, 10)

  // Create user
  try {
    const res = await fetch('https://api.example.com/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password: hashedPassword })
    })

    if (!res.ok) {
      const error = await res.json()
      return { error: error.message }
    }

    const user = await res.json()

    // Create session
    const session = await createSession(user.id)

    // Set cookie
    cookies().set('session', session.token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 7 // 7 days
    })

    redirect('/dashboard')

  } catch (error) {
    return { error: 'Signup failed' }
  }
}

export async function login(formData: FormData) {
  const email = formData.get('email') as string
  const password = formData.get('password') as string

  try {
    // Find user
    const res = await fetch(`https://api.example.com/users?email=${email}`)
    const user = await res.json()

    if (!user) {
      return { error: 'Invalid credentials' }
    }

    // Verify password
    const valid = await bcrypt.compare(password, user.password)

    if (!valid) {
      return { error: 'Invalid credentials' }
    }

    // Create session
    const session = await createSession(user.id)

    cookies().set('session', session.token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 7
    })

    redirect('/dashboard')

  } catch (error) {
    return { error: 'Login failed' }
  }
}

export async function logout() {
  cookies().delete('session')
  redirect('/login')
}

async function createSession(userId: string) {
  // Create session in database
  const res = await fetch('https://api.example.com/sessions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ userId })
  })

  return res.json()
}
```

**Signup Form:**

```typescript
// app/signup/page.tsx
import { signup } from '@/app/actions/auth'
import { SignupForm } from '@/components/SignupForm'

export default function SignupPage() {
  return (
    <div>
      <h1>Sign Up</h1>
      <SignupForm />
    </div>
  )
}

// components/SignupForm.tsx
'use client'

import { useFormState, useFormStatus } from 'react-dom'
import { signup } from '@/app/actions/auth'

function SubmitButton() {
  const { pending } = useFormStatus()
  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Signing up...' : 'Sign Up'}
    </button>
  )
}

export function SignupForm() {
  const [state, formAction] = useFormState(signup, null)

  return (
    <form action={formAction}>
      {state?.error && <p className="error">{state.error}</p>}

      <div>
        <label htmlFor="name">Name</label>
        <input type="text" id="name" name="name" required />
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input type="email" id="email" name="email" required />
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input type="password" id="password" name="password" required />
      </div>

      <SubmitButton />
    </form>
  )
}
```

**Login Form (similar structure):**

```typescript
// app/login/page.tsx
import { login } from '@/app/actions/auth'
import { LoginForm } from '@/components/LoginForm'

export default function LoginPage() {
  return (
    <div>
      <h1>Login</h1>
      <LoginForm />
    </div>
  )
}
```

**Protected Route Middleware:**

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const session = request.cookies.get('session')

  // Protected routes
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!session) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }

  // Redirect logged-in users away from auth pages
  if (request.nextUrl.pathname.startsWith('/login') ||
      request.nextUrl.pathname.startsWith('/signup')) {
    if (session) {
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/login', '/signup']
}
```

---

## Summary

These examples demonstrate:
- **Static Blog**: Force cache, dynamic routes, metadata
- **Dashboard**: No-store caching, Server/Client composition, parallel fetching
- **E-commerce**: ISR, Server Actions, shopping cart
- **Authentication**: Server Actions, cookies, middleware, protected routes

Refer to these patterns when building similar features in your Next.js 16 applications.
