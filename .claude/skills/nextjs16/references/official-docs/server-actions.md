# Next.js 16 Server Actions

This document covers Server Actions in Next.js 16, a powerful feature that allows server-side code execution directly from Client Components, eliminating the need for API routes in many cases.

## Overview

Server Actions are asynchronous server-side functions that can be called directly from Client Components or Server Components. They simplify data mutations, form handling, and server-side operations by removing the need to create separate API endpoints.

**Key Benefits:**
- Direct server function calls from components
- Built-in progressive enhancement for forms
- Automatic revalidation and redirects
- Type-safe with TypeScript
- No API route boilerplate needed

## Basic Server Action

### Creating a Server Action

Mark functions as Server Actions with the `'use server'` directive:

```typescript
// app/actions.ts
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  // Perform server-side operation
  await db.post.create({
    data: { title, content }
  })

  // Return result (optional)
  return { success: true }
}
```

### Using in a Form

```typescript
// app/posts/new/page.tsx
import { createPost } from '@/app/actions'

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input type="text" name="title" required />
      <textarea name="content" required />
      <button type="submit">Create Post</button>
    </form>
  )
}
```

**How it works:**
- Form submits to Server Action directly (no API route needed)
- Works without JavaScript (progressive enhancement)
- With JavaScript, submits via fetch (no page reload)

## Server Actions in Server Components

### Inline Server Action

Define Server Actions inline in Server Components:

```typescript
// app/posts/[id]/page.tsx
export default function PostPage({ params }: { params: { id: string } }) {
  async function deletePost() {
    'use server'

    await db.post.delete({
      where: { id: params.id }
    })

    redirect('/posts')
  }

  return (
    <div>
      <h1>Post {params.id}</h1>
      <form action={deletePost}>
        <button type="submit">Delete</button>
      </form>
    </div>
  )
}
```

### Separate Actions File

Organize Server Actions in a dedicated file:

```typescript
// app/actions/posts.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await db.post.create({
    data: { title, content }
  })

  revalidatePath('/posts')
  redirect('/posts')
}

export async function updatePost(id: string, formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await db.post.update({
    where: { id },
    data: { title, content }
  })

  revalidatePath(`/posts/${id}`)
  revalidatePath('/posts')
}

export async function deletePost(id: string) {
  await db.post.delete({ where: { id } })

  revalidatePath('/posts')
  redirect('/posts')
}
```

## Server Actions in Client Components

### With useFormState Hook

Add loading and error states to forms:

```typescript
// app/components/AddTodoForm.tsx
'use client'

import { useFormState, useFormStatus } from 'react-dom'
import { createTodo } from '@/app/actions'

const initialState = {
  message: '',
  success: false,
}

function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Adding...' : 'Add Todo'}
    </button>
  )
}

export function AddTodoForm() {
  const [state, formAction] = useFormState(createTodo, initialState)

  return (
    <form action={formAction}>
      <input type="text" name="todo" required />
      <SubmitButton />
      {state.message && (
        <p className={state.success ? 'success' : 'error'}>
          {state.message}
        </p>
      )}
    </form>
  )
}
```

```typescript
// app/actions.ts
'use server'

export async function createTodo(prevState: any, formData: FormData) {
  const todo = formData.get('todo') as string

  try {
    await db.todo.create({ data: { text: todo } })

    return {
      message: 'Todo created successfully!',
      success: true,
    }
  } catch (error) {
    return {
      message: 'Failed to create todo',
      success: false,
    }
  }
}
```

### With useFormStatus Hook

Show pending state during submission:

```typescript
'use client'

import { useFormStatus } from 'react-dom'

export function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" disabled={pending}>
      {pending ? (
        <>
          <Spinner />
          <span>Submitting...</span>
        </>
      ) : (
        'Submit'
      )}
    </button>
  )
}
```

### Calling Server Actions Programmatically

Call Server Actions from event handlers:

```typescript
'use client'

import { deletePost } from '@/app/actions'
import { useState } from 'react'

export function DeleteButton({ postId }: { postId: string }) {
  const [isDeleting, setIsDeleting] = useState(false)

  const handleDelete = async () => {
    if (!confirm('Are you sure?')) return

    setIsDeleting(true)
    try {
      await deletePost(postId)
    } catch (error) {
      alert('Failed to delete')
      setIsDeleting(false)
    }
  }

  return (
    <button onClick={handleDelete} disabled={isDeleting}>
      {isDeleting ? 'Deleting...' : 'Delete'}
    </button>
  )
}
```

## Form Handling Patterns

### Basic Form with Server Action

```typescript
// app/actions.ts
'use server'

export async function submitContact(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string
  const message = formData.get('message') as string

  await sendEmail({ name, email, message })

  return { success: true }
}

// app/contact/page.tsx
import { submitContact } from '@/app/actions'

export default function ContactPage() {
  return (
    <form action={submitContact}>
      <input type="text" name="name" placeholder="Name" required />
      <input type="email" name="email" placeholder="Email" required />
      <textarea name="message" placeholder="Message" required />
      <button type="submit">Send</button>
    </form>
  )
}
```

### Form with Validation

```typescript
// app/actions.ts
'use server'

import { z } from 'zod'

const CreatePostSchema = z.object({
  title: z.string().min(3).max(100),
  content: z.string().min(10),
})

export async function createPost(formData: FormData) {
  const rawData = {
    title: formData.get('title'),
    content: formData.get('content'),
  }

  // Validate
  const result = CreatePostSchema.safeParse(rawData)

  if (!result.success) {
    return {
      errors: result.error.flatten().fieldErrors,
      message: 'Validation failed',
    }
  }

  // Create post
  await db.post.create({
    data: result.data
  })

  revalidatePath('/posts')
  redirect('/posts')
}
```

### Form with Next.js Form Component

Next.js 16 provides a `Form` component with progressive enhancement:

```typescript
// app/users/new/page.tsx
import Form from 'next/form'
import { createUser } from '@/app/actions'

export default function NewUserPage() {
  return (
    <Form action={createUser}>
      <label htmlFor="name">Name</label>
      <input type="text" id="name" name="name" required />

      <label htmlFor="email">Email</label>
      <input type="email" id="email" name="email" required />

      <button type="submit">Create User</button>
    </Form>
  )
}
```

```typescript
// app/actions.ts
'use server'

import { redirect } from 'next/navigation'
import { revalidatePath } from 'next/cache'

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string

  await db.user.create({
    data: { name, email }
  })

  revalidatePath('/users')
  redirect('/users')
}
```

## Revalidation

### Revalidate by Path

Invalidate cached data for a specific route:

```typescript
'use server'

import { revalidatePath } from 'next/cache'

export async function updatePost(id: string, formData: FormData) {
  await db.post.update({ where: { id }, data: { /* ... */ } })

  // Revalidate specific paths
  revalidatePath(`/posts/${id}`) // Single post page
  revalidatePath('/posts') // Posts list page
}
```

### Revalidate by Tag

Invalidate cached data by tag:

```typescript
'use server'

import { revalidateTag } from 'next/cache'

export async function publishPost(id: string) {
  await db.post.update({
    where: { id },
    data: { published: true }
  })

  // Revalidate all requests tagged with 'posts'
  revalidateTag('posts')
}
```

**Fetching with tags:**

```typescript
// app/posts/page.tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { tags: ['posts'] }
  })
  return res.json()
}
```

## Redirects

Redirect after successful Server Action:

```typescript
'use server'

import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const post = await db.post.create({ data: { /* ... */ } })

  // Redirect to new post
  redirect(`/posts/${post.id}`)
}
```

## Authentication Example

Implement signup/login with Server Actions:

```typescript
// app/actions/auth.ts
'use server'

import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

export async function signup(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string
  const password = formData.get('password') as string

  // Hash password
  const hashedPassword = await bcrypt.hash(password, 10)

  // Create user
  const user = await db.user.create({
    data: { name, email, password: hashedPassword }
  })

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
}

export async function login(formData: FormData) {
  const email = formData.get('email') as string
  const password = formData.get('password') as string

  // Find user
  const user = await db.user.findUnique({ where: { email } })

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
}

export async function logout() {
  cookies().delete('session')
  redirect('/login')
}
```

```typescript
// app/signup/page.tsx
import { signup } from '@/app/actions/auth'

export default function SignupPage() {
  return (
    <form action={signup}>
      <input type="text" name="name" placeholder="Name" required />
      <input type="email" name="email" placeholder="Email" required />
      <input type="password" name="password" placeholder="Password" required />
      <button type="submit">Sign Up</button>
    </form>
  )
}
```

## Error Handling

### Try-Catch in Server Actions

```typescript
'use server'

export async function createPost(formData: FormData) {
  try {
    const title = formData.get('title') as string
    const content = formData.get('content') as string

    await db.post.create({
      data: { title, content }
    })

    revalidatePath('/posts')
    return { success: true }

  } catch (error) {
    console.error('Failed to create post:', error)

    return {
      success: false,
      error: 'Failed to create post. Please try again.'
    }
  }
}
```

### Display Errors in Client Component

```typescript
'use client'

import { useFormState } from 'react-dom'
import { createPost } from '@/app/actions'

export function CreatePostForm() {
  const [state, formAction] = useFormState(createPost, null)

  return (
    <form action={formAction}>
      <input type="text" name="title" required />
      <textarea name="content" required />
      <button type="submit">Create</button>

      {state?.error && (
        <div className="error">
          {state.error}
        </div>
      )}

      {state?.success && (
        <div className="success">
          Post created successfully!
        </div>
      )}
    </form>
  )
}
```

## Advanced Patterns

### Optimistic Updates

Update UI immediately, rollback on error:

```typescript
'use client'

import { useOptimistic } from 'react'
import { addTodo } from '@/app/actions'

export function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo: string) => [
      ...state,
      { id: Date.now(), text: newTodo, pending: true }
    ]
  )

  async function handleSubmit(formData: FormData) {
    const text = formData.get('todo') as string

    // Optimistic update
    addOptimisticTodo(text)

    // Server action
    await addTodo(formData)
  }

  return (
    <div>
      <ul>
        {optimisticTodos.map(todo => (
          <li key={todo.id} style={{ opacity: todo.pending ? 0.5 : 1 }}>
            {todo.text}
          </li>
        ))}
      </ul>

      <form action={handleSubmit}>
        <input type="text" name="todo" required />
        <button type="submit">Add</button>
      </form>
    </div>
  )
}
```

### File Uploads

Handle file uploads with Server Actions:

```typescript
'use server'

import { writeFile } from 'fs/promises'
import { join } from 'path'

export async function uploadFile(formData: FormData) {
  const file = formData.get('file') as File

  if (!file) {
    return { error: 'No file provided' }
  }

  // Convert to buffer
  const bytes = await file.arrayBuffer()
  const buffer = Buffer.from(bytes)

  // Save file
  const filename = `${Date.now()}-${file.name}`
  const path = join(process.cwd(), 'uploads', filename)

  await writeFile(path, buffer)

  return { success: true, filename }
}
```

```typescript
// app/upload/page.tsx
import { uploadFile } from '@/app/actions'

export default function UploadPage() {
  return (
    <form action={uploadFile}>
      <input type="file" name="file" required />
      <button type="submit">Upload</button>
    </form>
  )
}
```

## Best Practices

### 1. Validate Input

Always validate and sanitize input:

```typescript
'use server'

import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  age: z.number().min(0).max(120),
})

export async function updateProfile(formData: FormData) {
  const result = schema.safeParse({
    email: formData.get('email'),
    age: Number(formData.get('age')),
  })

  if (!result.success) {
    return { errors: result.error.errors }
  }

  // Continue with validated data
}
```

### 2. Use TypeScript

Type your Server Actions:

```typescript
'use server'

type CreatePostResult =
  | { success: true; postId: string }
  | { success: false; error: string }

export async function createPost(
  formData: FormData
): Promise<CreatePostResult> {
  try {
    const post = await db.post.create({ /* ... */ })
    return { success: true, postId: post.id }
  } catch (error) {
    return { success: false, error: 'Failed to create post' }
  }
}
```

### 3. Keep Actions Focused

One action, one responsibility:

```typescript
// ✅ Good: Separate actions
export async function createPost(formData: FormData) { /* ... */ }
export async function updatePost(id: string, formData: FormData) { /* ... */ }
export async function deletePost(id: string) { /* ... */ }

// ❌ Bad: Generic action doing everything
export async function handlePost(action: string, formData: FormData) { /* ... */ }
```

### 4. Revalidate Appropriately

Invalidate affected caches:

```typescript
export async function updatePost(id: string, formData: FormData) {
  await db.post.update({ /* ... */ })

  // Revalidate both list and detail pages
  revalidatePath('/posts')
  revalidatePath(`/posts/${id}`)
}
```

### 5. Handle Errors Gracefully

Return structured error information:

```typescript
export async function createPost(formData: FormData) {
  try {
    // Create post
    return { success: true }
  } catch (error) {
    if (error instanceof ValidationError) {
      return { success: false, errors: error.errors }
    }

    return { success: false, error: 'Something went wrong' }
  }
}
```

## Security Considerations

### 1. Validate on Server

Never trust client input:

```typescript
'use server'

export async function deletePost(id: string) {
  // Verify user has permission
  const session = await getSession()

  if (!session) {
    throw new Error('Unauthorized')
  }

  const post = await db.post.findUnique({ where: { id } })

  if (post.authorId !== session.userId) {
    throw new Error('Forbidden')
  }

  await db.post.delete({ where: { id } })
}
```

### 2. Use Environment Variables for Secrets

```typescript
'use server'

export async function sendEmail(formData: FormData) {
  // Use environment variable (never exposed to client)
  const apiKey = process.env.SENDGRID_API_KEY

  await sendgrid.send({
    apiKey,
    to: formData.get('email'),
    // ...
  })
}
```

### 3. Rate Limiting

Implement rate limiting for Server Actions:

```typescript
'use server'

import { ratelimit } from '@/lib/ratelimit'

export async function sendMessage(formData: FormData) {
  const identifier = await getUserIdentifier()

  const { success } = await ratelimit.limit(identifier)

  if (!success) {
    return { error: 'Rate limit exceeded' }
  }

  // Continue with action
}
```

## Summary

Server Actions in Next.js 16 provide:
- **Direct server-side execution** from components
- **Progressive enhancement** for forms
- **No API routes needed** for many use cases
- **Built-in revalidation** and redirect support
- **Type-safe** with TypeScript
- **Secure** by default (run only on server)

Use Server Actions for data mutations, form handling, and server-side operations to simplify your Next.js applications.
