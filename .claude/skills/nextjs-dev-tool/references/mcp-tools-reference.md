# MCP Tools Reference

Complete reference for all next-devtools-mcp tools with parameters, usage examples, and requirements.

## Tool Categories

### Runtime Diagnostic Tools
Require Next.js 16+ with running dev server:
- nextjs_index
- nextjs_call (with sub-tools)

### Standalone Tools
Work without running server:
- init
- nextjs_docs
- browser_eval
- upgrade_nextjs_16
- enable_cache_components

---

## init

**Purpose:** Initialize Next.js DevTools context for AI assistants

**Parameters:**
- `project_path` (optional) - Defaults to current directory

**Capabilities:**
- Establishes Next.js development context
- Documents available MCP tools and use cases
- Provides best practices
- Shows example workflows

**When to Use:**
At the beginning of any Next.js development session

**Example:**
```typescript
// Call init tool to set up context
{
  "project_path": "/path/to/nextjs-project"
}
```

**Output:**
- Available tools list
- Best practices documentation
- Workflow examples

---

## nextjs_index

**Purpose:** Discover all running Next.js dev servers and their available tools

**Parameters:** None required

**Capabilities:**
- Auto-detects Next.js 16+ dev servers on your machine
- Scans ports 3000-3010
- Lists runtime diagnostic tools from each server's MCP endpoint (`/_next/mcp`)

**Available Runtime Tools:**
- `get_errors` - Current build, runtime, and type errors
- `get_logs` - Path to development log file
- `get_page_metadata` - Routes, pages, component metadata
- `get_project_metadata` - Project structure, config, dev server URL
- `get_server_action_by_id` - Look up Server Actions by ID

**Requirements:**
- Next.js 16+
- Running dev server

**Example:**
```bash
# Just invoke the tool
# No parameters needed
```

**Output:**
```json
{
  "servers": [
    {
      "port": 3000,
      "project": "/path/to/project",
      "tools": [
        "get_errors",
        "get_logs",
        "get_page_metadata",
        "get_project_metadata",
        "get_server_action_by_id"
      ]
    }
  ]
}
```

---

## nextjs_call

**Purpose:** Execute a specific MCP tool on a running Next.js dev server

**Parameters:**
- `port` (required) - Dev server port from `nextjs_index`
- `toolName` (required) - Name of the tool to invoke
- `args` (optional) - Arguments object if the tool requires parameters

**Requirements:**
- Next.js 16+
- Running dev server
- Use `nextjs_index` first to discover servers

**Workflow:**
1. Call `nextjs_index` to discover servers
2. Call `nextjs_call` with port and toolName

**Example:**
```typescript
// Get errors from server on port 3000
{
  "port": 3000,
  "toolName": "get_errors"
}

// Get page metadata with arguments
{
  "port": 3000,
  "toolName": "get_page_metadata",
  "args": {
    "path": "/dashboard"
  }
}
```

---

## Sub-Tools via nextjs_call

### get_errors

**Purpose:** Retrieve current build, runtime, and type errors

**Parameters:** None

**Returns:**
```json
{
  "buildErrors": [],
  "runtimeErrors": [],
  "typeErrors": []
}
```

**Use For:**
- Quick error checking
- Pre-deployment validation
- Continuous monitoring during development

### get_logs

**Purpose:** Get path to development log file

**Parameters:** None

**Returns:**
```json
{
  "logPath": "/path/to/.next/logs/dev.log"
}
```

**Usage After:**
```bash
tail -f /path/to/.next/logs/dev.log
```

### get_page_metadata

**Purpose:** Get metadata about application pages, routes, and components

**Parameters:**
- `path` (optional) - Specific route path to inspect

**Returns:**
```json
{
  "routes": [
    {
      "path": "/dashboard",
      "component": "app/dashboard/page.tsx",
      "layout": "app/layout.tsx",
      "metadata": {...}
    }
  ]
}
```

**Use For:**
- Verifying routes exist
- Understanding component hierarchy
- Checking metadata configuration

### get_project_metadata

**Purpose:** Retrieve project structure, configuration, and dev server information

**Parameters:** None

**Returns:**
```json
{
  "structure": {...},
  "config": {...},
  "devServerUrl": "http://localhost:3000"
}
```

**Use For:**
- Understanding project setup
- Checking configuration
- Verifying dev server status

### get_server_action_by_id

**Purpose:** Look up Server Action details by ID

**Parameters:**
- `id` (required) - Server Action ID

**Returns:**
```json
{
  "id": "action_123",
  "name": "submitForm",
  "file": "app/actions.ts",
  "line": 42
}
```

**Use For:**
- Debugging form submissions
- Tracing Server Action calls
- Verifying action bindings

---

## nextjs_docs

**Purpose:** Search and retrieve official Next.js documentation

**Parameters:**
- `action` (required) - `search` or `get`
- `query` (optional) - Required for search (e.g., 'metadata', 'middleware')
- `path` (optional) - Required for get (e.g., '/docs/app/api-reference/functions/refresh')
- `anchor` (optional) - Section reference from search results
- `routerType` (optional) - `app`, `pages`, or `all` (default: all)

**Two-Step Process:**

**Step 1: Search**
```typescript
{
  "action": "search",
  "query": "metadata",
  "routerType": "app"
}
```

**Step 2: Get**
```typescript
{
  "action": "get",
  "path": "/docs/app/api-reference/functions/generate-metadata",
  "anchor": "parameters"
}
```

**Use For:**
- Looking up API references
- Finding implementation examples
- Understanding best practices
- Checking migration guides

---

## browser_eval

**Purpose:** Automate and test web applications using Playwright

**Parameters:**
- `action` (required)
- `browser` (optional) - `chrome`, `firefox`, `webkit`, `msedge` (default: chrome)
- `headless` (optional) - Run headless (default: true)
- Action-specific parameters

**Available Actions:**

### start
Initialize browser automation

```typescript
{
  "action": "start",
  "browser": "chrome",
  "headless": true
}
```

### navigate
Go to a URL

```typescript
{
  "action": "navigate",
  "url": "http://localhost:3000/dashboard"
}
```

### click
Click an element

```typescript
{
  "action": "click",
  "selector": "button[type='submit']"
}
```

### type
Enter text in input

```typescript
{
  "action": "type",
  "selector": "input[name='email']",
  "text": "user@example.com"
}
```

### screenshot
Capture page visual

```typescript
{
  "action": "screenshot",
  "path": "./screenshots/dashboard.png"
}
```

### console_messages
Retrieve browser console output

```typescript
{
  "action": "console_messages"
}
```

**Returns:**
```json
{
  "messages": [
    {"type": "error", "text": "Hydration failed"},
    {"type": "warning", "text": "Missing key prop"}
  ]
}
```

### evaluate
Execute JavaScript in browser

```typescript
{
  "action": "evaluate",
  "script": "document.title"
}
```

### close
Shut down browser

```typescript
{
  "action": "close"
}
```

**Additional Actions:**
- `drag` - Perform drag-and-drop
- `upload_file` - Handle file uploads
- `fill_form` - Populate multiple form fields
- `list_tools` - Display available actions

**Use For:**
- Visual verification
- Runtime error detection
- User flow testing
- Console error capture

---

## upgrade_nextjs_16

**Purpose:** Guide upgrading Next.js to version 16 with automated codemod execution

**Parameters:**
- `project_path` (optional) - Defaults to current directory

**Capabilities:**
- Runs official Next.js codemod automatically
- Handles async API changes (params, searchParams, cookies, headers)
- Migrates configuration changes
- Updates image defaults
- Fixes parallel routes and dynamic segments
- Handles deprecated API removals
- Provides React 19 compatibility guidance

**Requirements:**
- Clean git state (no uncommitted changes)
- Backup recommended

**Output:**
Structured JSON with step-by-step upgrade guidance

**Example:**
```typescript
{
  "project_path": "/path/to/nextjs-project"
}
```

**Handles:**
- `async params` migration
- `async searchParams` migration
- `async cookies()` migration
- `async headers()` migration
- Configuration file updates
- Deprecated API removals

---

## enable_cache_components

**Purpose:** Complete Cache Components setup and migration for Next.js 16

**Parameters:**
- `project_path` (optional) - Defaults to current directory

**Capabilities:**
- Pre-flight checks (package manager, version, config)
- Enable Cache Components configuration
- Start dev server with MCP enabled
- Automated route verification
- Error detection and fixing
- Automated boundary setup (Suspense, caching directives, static params)
- Final verification and build testing

**Process Phases:**
1. **Pre-flight** - Verify requirements
2. **Configuration** - Enable in next.config.js
3. **Dev Server** - Start with MCP
4. **Verification** - Check all routes
5. **Error Detection** - Find caching issues
6. **Automated Fixing** - Apply boundaries
7. **Final Testing** - Verify and build

**Output:**
Structured JSON with complete setup guidance

**Example:**
```typescript
{
  "project_path": "/path/to/nextjs-project"
}
```

---

## Error Responses

All tools return errors in this format:

```json
{
  "error": true,
  "message": "Descriptive error message",
  "code": "ERROR_CODE"
}
```

**Common Error Codes:**
- `SERVER_NOT_FOUND` - Dev server not running
- `TOOL_NOT_AVAILABLE` - Tool doesn't exist
- `INVALID_PARAMS` - Missing or invalid parameters
- `VERSION_MISMATCH` - Next.js version < 16
- `GIT_DIRTY` - Uncommitted changes (for codemods)

---

## Best Practices

1. **Always call `nextjs_index` first** - Know what servers are available
2. **Check return values** - Handle errors appropriately
3. **Use specific tools** - Don't use browser_eval when MCP tools exist
4. **Keep dev server running** - Required for most diagnostic tools
5. **Monitor console output** - Use browser_eval for client-side errors
6. **Clean git state** - Required for codemods
7. **Test incrementally** - Verify after each change
