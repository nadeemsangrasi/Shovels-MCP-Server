# Integration Guides

## Integration with Other Skills

### Integration with better-auth-nextjs

When setting up authentication using the better-auth-nextjs skill, use nextjs-dev-tool to enhance your development workflow.

#### Verify Auth Routes

After setting up better-auth, verify all routes are registered:

```typescript
// Check all routes exist
nextjs_call({
  "port": 3000,
  "toolName": "get_page_metadata"
})

// Verify:
// - /sign-in page
// - /sign-up page
// - /api/auth/[...all] route
// - /dashboard (protected route)
```

#### Debug Middleware Configuration

Check middleware is properly configured:

```typescript
// Get project metadata
nextjs_call({
  "port": 3000,
  "toolName": "get_project_metadata"
})

// Verify middleware.ts exists and is configured
```

#### Test Authentication Flows

Use browser automation to test sign-in/sign-up:

```typescript
// Start browser
browser_eval({ "action": "start" })

// Test sign-in
browser_eval({
  "action": "navigate",
  "url": "http://localhost:3000/sign-in"
})

// Fill credentials
browser_eval({
  "action": "type",
  "selector": "input[name='email']",
  "text": "test@example.com"
})

browser_eval({
  "action": "type",
  "selector": "input[name='password']",
  "text": "password123"
})

// Submit
browser_eval({
  "action": "click",
  "selector": "button[type='submit']"
})

// Verify redirect to dashboard
browser_eval({
  "action": "evaluate",
  "script": "window.location.pathname"
})
// Should return "/dashboard"

// Check for errors
browser_eval({ "action": "console_messages" })

browser_eval({ "action": "close" })
```

#### Check for Hydration Errors

Auth components often cause hydration issues:

```typescript
// Get errors
nextjs_call({
  "port": 3000,
  "toolName": "get_errors"
})

// Also check browser console
browser_eval({
  "action": "navigate",
  "url": "http://localhost:3000/sign-in"
})

browser_eval({ "action": "console_messages" })
```

**Common hydration fixes:**
- Add `'use client'` to components using `useSession`
- Wrap auth state in Suspense boundaries
- Use dynamic imports for client-only code

#### Verify Protected Routes

Test middleware protection:

```typescript
// Clear session (incognito or clear cookies)
browser_eval({ "action": "start" })

// Try accessing protected route
browser_eval({
  "action": "navigate",
  "url": "http://localhost:3000/dashboard"
})

// Verify redirect to sign-in
browser_eval({
  "action": "evaluate",
  "script": "window.location.pathname"
})
// Should return "/sign-in"

browser_eval({ "action": "close" })
```

#### Complete Auth Verification Workflow

```typescript
// 1. Check all auth routes exist
nextjs_call({ /* get_page_metadata */ })

// 2. Verify no build errors
nextjs_call({ /* get_errors */ })

// 3. Test sign-up flow
browser_eval({ /* test sign-up */ })

// 4. Test sign-in flow
browser_eval({ /* test sign-in */ })

// 5. Test protected routes
browser_eval({ /* test dashboard */ })

// 6. Test sign-out
browser_eval({ /* test sign-out */ })

// 7. Verify middleware
browser_eval({ /* test unauthorized access */ })
```

---

### Integration with nextjs16 Skill

Complement Next.js 16 development with dev tools:

#### Verify New Features

After adding new features with nextjs16 skill:

```typescript
// Check routes are registered
nextjs_call({
  "port": 3000,
  "toolName": "get_page_metadata"
})

// Look for your new routes
```

#### Debug Routing Issues

When routes don't work as expected:

```typescript
// Get all routes
nextjs_call({ /* get_page_metadata */ })

// Check logs for routing errors
nextjs_call({ /* get_logs */ })

// Test route in browser
browser_eval({
  "action": "navigate",
  "url": "http://localhost:3000/your-route"
})

browser_eval({ "action": "console_messages" })
```

#### Test Metadata Configuration

Verify metadata from generateMetadata:

```typescript
// Navigate to page
browser_eval({
  "action": "navigate",
  "url": "http://localhost:3000/page"
})

// Check metadata
browser_eval({
  "action": "evaluate",
  "script": "document.title"
})

browser_eval({
  "action": "evaluate",
  "script": "document.querySelector('meta[name=\"description\"]').content"
})
```

#### Verify Server Components

Check Server Components are working:

```typescript
// Check for hydration errors
nextjs_call({ /* get_errors */ })

// Browser console should not show client-side errors
browser_eval({ /* console_messages */ })
```

#### Test New API Routes

Verify API routes work correctly:

```typescript
// Use browser_eval to test
browser_eval({
  "action": "evaluate",
  "script": `
    fetch('/api/data')
      .then(r => r.json())
      .then(console.log)
  `
})

// Check console for response
browser_eval({ "action": "console_messages" })
```

---

### Integration with Drizzle ORM

When working with database queries:

#### Debug Database Connection Errors

```typescript
// Check errors
nextjs_call({
  "port": 3000,
  "toolName": "get_errors"
})

// Review logs for database errors
nextjs_call({
  "port": 3000,
  "toolName": "get_logs"
})
```

#### Test Data Fetching

```typescript
// Navigate to page with data
browser_eval({
  "action": "navigate",
  "url": "http://localhost:3000/dashboard"
})

// Check if data loaded
browser_eval({
  "action": "evaluate",
  "script": "document.querySelector('[data-testid=\"user-name\"]').textContent"
})

// Check for query errors
browser_eval({ "action": "console_messages" })
```

---

### Integration with TypeScript

#### Verify Type Errors

```typescript
// Get type errors
nextjs_call({
  "port": 3000,
  "toolName": "get_errors"
})

// Output will include TypeScript errors
```

#### Check Generated Types

```typescript
// Get project metadata
nextjs_call({
  "port": 3000,
  "toolName": "get_project_metadata"
})

// Verify TypeScript is enabled
```

---

### Integration with Tailwind CSS

#### Verify Styles Applied

```typescript
// Navigate to styled page
browser_eval({
  "action": "navigate",
  "url": "http://localhost:3000"
})

// Take screenshot
browser_eval({
  "action": "screenshot",
  "path": "./screenshots/styled-page.png"
})

// Check computed styles
browser_eval({
  "action": "evaluate",
  "script": "getComputedStyle(document.querySelector('.button')).backgroundColor"
})
```

---

### Integration with Environment Variables

#### Verify Environment Variables Loaded

```typescript
// Get project metadata
nextjs_call({
  "port": 3000,
  "toolName": "get_project_metadata"
})

// Check logs for env var related errors
nextjs_call({
  "port": 3000,
  "toolName": "get_logs"
})
```

---

## Cross-Skill Workflows

### Full Stack Development Workflow

**Scenario:** Building a feature from scratch

```typescript
// 1. Create components (nextjs16 skill)
// 2. Add authentication (better-auth-nextjs skill)
// 3. Verify routes (nextjs-dev-tool)
nextjs_call({ /* get_page_metadata */ })

// 4. Check for errors
nextjs_call({ /* get_errors */ })

// 5. Test in browser
browser_eval({ /* full test flow */ })

// 6. Verify documentation
nextjs_docs({ /* lookup as needed */ })
```

### Debugging Workflow

**Scenario:** Something's not working

```typescript
// 1. Check errors (nextjs-dev-tool)
nextjs_call({ /* get_errors */ })

// 2. Review logs
nextjs_call({ /* get_logs */ })

// 3. Test in browser
browser_eval({ /* console_messages */ })

// 4. Query docs for solution (nextjs-dev-tool)
nextjs_docs({ /* search for answers */ })

// 5. Apply fix (nextjs16 or better-auth-nextjs)

// 6. Verify fix (nextjs-dev-tool)
browser_eval({ /* verify */ })
```

### Pre-Deployment Workflow

**Scenario:** Preparing for production

```typescript
// 1. Verify all routes (nextjs-dev-tool)
nextjs_call({ /* get_page_metadata */ })

// 2. Check for errors
nextjs_call({ /* get_errors */ })

// 3. Test authentication flows (if using better-auth-nextjs)
browser_eval({ /* auth tests */ })

// 4. Test critical pages
browser_eval({ /* page tests */ })

// 5. Review project config
nextjs_call({ /* get_project_metadata */ })

// 6. Final screenshot verification
browser_eval({ /* screenshots */ })
```

---

## Tips for Multi-Skill Integration

1. **Use nextjs-dev-tool for verification** after making changes with other skills
2. **Browser automation is key** - Visual verification catches issues docs miss
3. **Check both server and client errors** - Use get_errors AND browser_eval
4. **Query docs contextually** - When stuck, use nextjs_docs from this skill
5. **Test incrementally** - Verify after each major change
6. **Keep dev server running** - Required for most nextjs-dev-tool features
7. **Cross-reference documentation** - Each skill has relevant guides

---

## Skill Combination Examples

### better-auth-nextjs + nextjs-dev-tool

**Best for:** Setting up and debugging authentication

**Workflow:**
1. Use better-auth-nextjs to set up auth
2. Use nextjs-dev-tool to verify routes
3. Use nextjs-dev-tool to test auth flows
4. Use nextjs-dev-tool to debug errors

### nextjs16 + nextjs-dev-tool

**Best for:** Building and testing new features

**Workflow:**
1. Use nextjs16 to create features
2. Use nextjs-dev-tool to verify implementation
3. Use nextjs-dev-tool to test in browser
4. Use nextjs-dev-tool to debug issues

### All Three Skills Together

**Best for:** Full-stack Next.js development

**Workflow:**
1. Use nextjs16 for base setup
2. Use better-auth-nextjs for authentication
3. Use nextjs-dev-tool throughout for:
   - Verification
   - Testing
   - Debugging
   - Documentation lookups
