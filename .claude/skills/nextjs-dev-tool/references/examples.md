# Complete Examples

## Quick Error Check

**Scenario:** Check if there are any errors in your Next.js app

**Workflow:**
```typescript
// 1. Discover servers
nextjs_index()

// Output:
{
  "servers": [{
    "port": 3000,
    "project": "/path/to/project",
    "tools": ["get_errors", "get_logs", ...]
  }]
}

// 2. Get errors from discovered server
nextjs_call({
  "port": 3000,
  "toolName": "get_errors"
})

// Output:
{
  "buildErrors": [],
  "runtimeErrors": [
    {
      "message": "Hydration failed",
      "file": "app/dashboard/page.tsx",
      "line": 42
    }
  ],
  "typeErrors": []
}
```

**Result:** Identified hydration error in dashboard page

---

## Route Check

**Scenario:** Verify all routes are properly registered

**Workflow:**
```typescript
// Get all page metadata
nextjs_call({
  "port": 3000,
  "toolName": "get_page_metadata"
})

// Output:
{
  "routes": [
    {
      "path": "/",
      "component": "app/page.tsx",
      "layout": "app/layout.tsx"
    },
    {
      "path": "/dashboard",
      "component": "app/dashboard/page.tsx",
      "layout": "app/layout.tsx"
    },
    {
      "path": "/dashboard/settings",
      "component": "app/dashboard/settings/page.tsx",
      "layout": "app/dashboard/layout.tsx"
    }
  ]
}
```

**Verification:** All expected routes are present with correct component mappings

---

## Browser Testing

**Scenario:** Test sign-in flow and check for console errors

**Workflow:**
```typescript
// 1. Start browser
browser_eval({
  "action": "start",
  "browser": "chrome",
  "headless": false  // Set true for CI
})

// 2. Navigate to sign-in page
browser_eval({
  "action": "navigate",
  "url": "http://localhost:3000/sign-in"
})

// 3. Fill in form
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

// 4. Submit form
browser_eval({
  "action": "click",
  "selector": "button[type='submit']"
})

// 5. Take screenshot
browser_eval({
  "action": "screenshot",
  "path": "./screenshots/after-signin.png"
})

// 6. Check console messages
browser_eval({
  "action": "console_messages"
})

// Output:
{
  "messages": [
    {"type": "log", "text": "Form submitted"},
    {"type": "error", "text": "Failed to fetch user data"}
  ]
}

// 7. Close browser
browser_eval({
  "action": "close"
})
```

**Result:** Identified API error during sign-in

---

## Documentation Lookup

**Scenario:** Find information about middleware configuration

**Workflow:**
```typescript
// 1. Search docs
nextjs_docs({
  "action": "search",
  "query": "middleware configuration",
  "routerType": "app"
})

// Output:
{
  "results": [
    {
      "title": "Middleware",
      "path": "/docs/app/building-your-application/routing/middleware",
      "snippet": "Middleware allows you to run code before a request is completed..."
    }
  ]
}

// 2. Get full content
nextjs_docs({
  "action": "get",
  "path": "/docs/app/building-your-application/routing/middleware"
})

// Output: Full markdown content of the middleware documentation
```

**Result:** Found official documentation for middleware setup

---

## Project Metadata

**Scenario:** Understand project structure and configuration

**Workflow:**
```typescript
nextjs_call({
  "port": 3000,
  "toolName": "get_project_metadata"
})

// Output:
{
  "structure": {
    "appDirectory": true,
    "pagesDirectory": false,
    "srcDirectory": false,
    "publicDirectory": true
  },
  "config": {
    "typescript": true,
    "eslint": true,
    "reactStrictMode": true,
    "experimental": {
      "cacheComponents": true
    }
  },
  "devServerUrl": "http://localhost:3000",
  "nextVersion": "16.1.0"
}
```

**Result:** Confirmed App Router setup with Cache Components enabled

---

## Log Access

**Scenario:** Monitor development logs for detailed error information

**Workflow:**
```typescript
// 1. Get log path
nextjs_call({
  "port": 3000,
  "toolName": "get_logs"
})

// Output:
{
  "logPath": "/path/to/project/.next/logs/dev.log"
}

// 2. Read logs (using Bash tool)
tail -f /path/to/project/.next/logs/dev.log

// Log output:
[18:30:15] Compiling /dashboard page...
[18:30:16] ✓ Compiled /dashboard in 1.2s
[18:30:20] ⨯ Error: Database connection failed
[18:30:20]   at connectDB (lib/db.ts:15:10)
```

**Result:** Identified database connection error with stack trace

---

## Server Action Debugging

**Scenario:** Debug a failing Server Action by ID

**Workflow:**
```typescript
// From browser console or error log, you have:
// Server Action ID: "abc123def456"

nextjs_call({
  "port": 3000,
  "toolName": "get_server_action_by_id",
  "args": {
    "id": "abc123def456"
  }
})

// Output:
{
  "id": "abc123def456",
  "name": "submitForm",
  "file": "app/actions/form.ts",
  "line": 42,
  "type": "server-action"
}
```

**Result:** Located Server Action in codebase for debugging

---

## Full Debug Session

**Scenario:** Complete debugging workflow from error detection to fix verification

**Workflow:**
```typescript
// 1. Discover servers
nextjs_index()
// Found server on port 3000

// 2. Check for errors
nextjs_call({
  "port": 3000,
  "toolName": "get_errors"
})
// Found: Hydration error in /dashboard

// 3. Get detailed logs
nextjs_call({
  "port": 3000,
  "toolName": "get_logs"
})
// Log path: .next/logs/dev.log

// 4. Read logs
tail -f .next/logs/dev.log
// Detailed error: useEffect hook in client component

// 5. Fix the issue (add 'use client' directive)

// 6. Verify with browser test
browser_eval({ "action": "start" })
browser_eval({
  "action": "navigate",
  "url": "http://localhost:3000/dashboard"
})
browser_eval({ "action": "console_messages" })
// No errors!

browser_eval({ "action": "screenshot", "path": "./verified.png" })
browser_eval({ "action": "close" })

// 7. Final error check
nextjs_call({
  "port": 3000,
  "toolName": "get_errors"
})
// Output: No errors found
```

**Result:** Successfully debugged and verified fix

---

## Pre-Deployment Checklist

**Scenario:** Verify app is ready for deployment

**Workflow:**
```typescript
// 1. Check all errors are resolved
nextjs_call({
  "port": 3000,
  "toolName": "get_errors"
})
// ✓ No errors

// 2. Verify all routes
nextjs_call({
  "port": 3000,
  "toolName": "get_page_metadata"
})
// ✓ All routes registered

// 3. Test critical pages
browser_eval({ "action": "start" })

// Test homepage
browser_eval({ "action": "navigate", "url": "http://localhost:3000" })
browser_eval({ "action": "screenshot", "path": "./screenshots/homepage.png" })

// Test dashboard
browser_eval({ "action": "navigate", "url": "http://localhost:3000/dashboard" })
browser_eval({ "action": "screenshot", "path": "./screenshots/dashboard.png" })

// Check console
browser_eval({ "action": "console_messages" })
// ✓ No errors or warnings

browser_eval({ "action": "close" })

// 4. Verify project config
nextjs_call({
  "port": 3000,
  "toolName": "get_project_metadata"
})
// ✓ Production-ready configuration
```

**Result:** All checks passed, ready for deployment

---

## Upgrade to Next.js 16

**Scenario:** Upgrade existing project to Next.js 16

**Workflow:**
```typescript
// 1. Ensure clean git state
git status
// ✓ No uncommitted changes

// 2. Run upgrade tool
upgrade_nextjs_16({
  "project_path": "/path/to/project"
})

// Output:
{
  "steps": [
    "✓ Updated package.json to next@16.1.0",
    "✓ Installed dependencies",
    "✓ Running codemod for async APIs",
    "  - Modified app/dashboard/page.tsx",
    "  - Modified app/api/route.ts",
    "✓ Updated next.config.js",
    "! Review changes and test your app"
  ]
}

// 3. Start dev server
npm run dev

// 4. Check for errors
nextjs_index()
nextjs_call({
  "port": 3000,
  "toolName": "get_errors"
})
// Address any migration issues

// 5. Test thoroughly
browser_eval({ /* full test suite */ })
```

**Result:** Successfully upgraded to Next.js 16

---

## Enable Cache Components

**Scenario:** Set up Cache Components in Next.js 16 project

**Workflow:**
```typescript
enable_cache_components({
  "project_path": "/path/to/project"
})

// Output (phase-by-phase):
{
  "phase": "pre-flight",
  "checks": [
    "✓ Package manager: npm",
    "✓ Next.js version: 16.1.0",
    "✓ Configuration writable"
  ]
}

{
  "phase": "configuration",
  "actions": [
    "✓ Enabled cacheComponents in next.config.js",
    "✓ Configuration validated"
  ]
}

{
  "phase": "dev-server",
  "status": "Starting dev server with MCP..."
}

{
  "phase": "verification",
  "routes": [
    "✓ / - No issues",
    "✗ /dashboard - Missing Suspense boundary",
    "✗ /api/data - Needs static params"
  ]
}

{
  "phase": "automated-fixing",
  "fixes": [
    "✓ Added Suspense boundary to /dashboard",
    "✓ Added generateStaticParams to /api/data"
  ]
}

{
  "phase": "final-verification",
  "status": "All routes working correctly"
}
```

**Result:** Cache Components enabled and working

---

## Integration with Authentication

**Scenario:** Debug authentication setup from better-auth-nextjs skill

**Workflow:**
```typescript
// 1. Verify auth routes exist
nextjs_call({
  "port": 3000,
  "toolName": "get_page_metadata"
})
// Check for: /sign-in, /sign-up, /api/auth/[...all]

// 2. Test sign-in flow
browser_eval({ "action": "start" })
browser_eval({
  "action": "navigate",
  "url": "http://localhost:3000/sign-in"
})

// Fill form and submit
browser_eval({ /* form submission */ })

// 3. Check for hydration errors (common with auth)
browser_eval({ "action": "console_messages" })

// 4. Verify middleware is working
nextjs_call({
  "port": 3000,
  "toolName": "get_project_metadata"
})
// Check middleware.ts configuration

// 5. Test protected route
browser_eval({
  "action": "navigate",
  "url": "http://localhost:3000/dashboard"
})
// Should redirect to /sign-in if not authenticated

browser_eval({ "action": "close" })
```

**Result:** Verified authentication flow working correctly
