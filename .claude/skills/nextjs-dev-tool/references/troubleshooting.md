# Troubleshooting Guide

## Common Issues and Solutions

### No Servers Found

**Error:** `nextjs_index` returns empty servers array

**Causes:**
- Dev server not running
- Next.js version < 16
- Server on non-standard port
- MCP endpoint not enabled

**Solutions:**
1. **Start dev server:**
   ```bash
   npm run dev
   # or
   pnpm dev
   # or
   yarn dev
   ```

2. **Check Next.js version:**
   ```bash
   npm list next
   # Must be 16.0.0 or higher
   ```

3. **Verify MCP endpoint:**
   ```bash
   curl http://localhost:3000/_next/mcp
   # Should return MCP endpoint info
   ```

4. **Check if server is on different port:**
   ```bash
   lsof -i :3000
   lsof -i :3001
   # etc.
   ```

---

### Connection Refused

**Error:** `ECONNREFUSED` when calling `nextjs_call`

**Causes:**
- Wrong port number
- Dev server crashed
- Firewall blocking connection

**Solutions:**
1. **Verify correct port:**
   ```typescript
   // Always run nextjs_index first
   nextjs_index()
   // Use port from output
   ```

2. **Restart dev server:**
   ```bash
   # Kill existing process
   lsof -ti:3000 | xargs kill -9
   # Start fresh
   npm run dev
   ```

3. **Check firewall:**
   - Ensure localhost connections allowed
   - Check antivirus software

---

### Tool Not Available

**Error:** `Tool 'get_errors' not available`

**Causes:**
- Next.js version < 16
- Dev server not fully started
- MCP not enabled in configuration

**Solutions:**
1. **Upgrade Next.js:**
   ```bash
   npm install next@latest
   # or use upgrade_nextjs_16 tool
   ```

2. **Wait for server to fully start:**
   - Look for "Ready" message in terminal
   - Can take 10-30 seconds on first start

3. **Verify next.config.js:**
   ```javascript
   // MCP is enabled by default in Next.js 16+
   // No configuration needed
   ```

---

### MCP Endpoint 404

**Error:** `404 Not Found` at `/_next/mcp`

**Causes:**
- Next.js version < 16
- Server not in development mode
- Custom server setup interfering

**Solutions:**
1. **Check version:**
   ```bash
   npm list next
   ```

2. **Ensure development mode:**
   ```bash
   npm run dev
   # NOT: npm run start (production)
   ```

3. **Check for custom server:**
   - MCP endpoint only works with standard Next.js dev server
   - Custom servers need additional configuration

---

### Codemod Failed

**Error:** `Git working directory not clean` or codemod exits with error

**Causes:**
- Uncommitted changes
- Merge conflicts
- File permissions

**Solutions:**
1. **Commit or stash changes:**
   ```bash
   git add .
   git commit -m "Pre-upgrade commit"
   # or
   git stash
   ```

2. **Resolve merge conflicts:**
   ```bash
   git status
   # Resolve any conflicts
   ```

3. **Check file permissions:**
   ```bash
   ls -la
   # Ensure files are writable
   ```

---

### Browser Automation Failed

**Error:** Playwright installation or execution failed

**Causes:**
- Playwright not installed
- Missing system dependencies
- Headless mode not supported

**Solutions:**
1. **Install Playwright:**
   ```bash
   # Usually auto-installed on first use
   # Manual installation:
   npx playwright install
   ```

2. **Install system dependencies:**
   ```bash
   # Ubuntu/Debian
   npx playwright install-deps

   # macOS
   # Usually no additional deps needed

   # Windows
   # Usually no additional deps needed
   ```

3. **Try different browser:**
   ```typescript
   browser_eval({
     "action": "start",
     "browser": "firefox"  // or "webkit"
   })
   ```

4. **Disable headless mode:**
   ```typescript
   browser_eval({
     "action": "start",
     "headless": false
   })
   ```

---

### Documentation Search Returns No Results

**Error:** `nextjs_docs` search returns empty results

**Causes:**
- Typo in search query
- Filtering by wrong router type
- Query too specific

**Solutions:**
1. **Try broader query:**
   ```typescript
   // Instead of:
   {"query": "generateMetadata with params"}

   // Try:
   {"query": "metadata"}
   ```

2. **Check router filter:**
   ```typescript
   {
     "action": "search",
     "query": "metadata",
     "routerType": "all"  // Not just "app" or "pages"
   }
   ```

3. **Search different terms:**
   - Try alternative keywords
   - Use official terminology from docs

---

### Errors Not Detected

**Error:** `get_errors` returns empty but app has visible errors

**Causes:**
- Runtime errors not in server context
- Client-side only errors
- Errors in external dependencies

**Solutions:**
1. **Use browser_eval for client errors:**
   ```typescript
   browser_eval({
     "action": "console_messages"
   })
   ```

2. **Check dev server logs:**
   ```typescript
   nextjs_call({
     "port": 3000,
     "toolName": "get_logs"
   })
   // Then read log file
   ```

3. **Look for hydration errors:**
   - Often client-side only
   - Check browser console
   - Use `browser_eval` to capture

---

### Cache Components Setup Failed

**Error:** `enable_cache_components` fails during setup

**Causes:**
- Configuration file syntax error
- Incompatible dependencies
- Routes with dynamic requirements

**Solutions:**
1. **Check next.config.js syntax:**
   ```javascript
   // Must be valid JavaScript
   // Use proper ESM or CommonJS format
   ```

2. **Update dependencies:**
   ```bash
   npm update
   # Ensure compatible versions
   ```

3. **Review route requirements:**
   - Some routes may need Suspense boundaries
   - Dynamic routes need generateStaticParams
   - Follow error messages from tool

---

### Server Action Not Found

**Error:** `get_server_action_by_id` returns null

**Causes:**
- Invalid Server Action ID
- Server Action not registered
- Build cache out of date

**Solutions:**
1. **Verify ID format:**
   - Should be a long alphanumeric string
   - Get from browser devtools or error logs

2. **Rebuild:**
   ```bash
   rm -rf .next
   npm run dev
   ```

3. **Check Server Action export:**
   ```typescript
   // Must have 'use server' directive
   'use server'

   export async function myAction() {
     // ...
   }
   ```

---

## Debug Checklist

When encountering issues:

- [ ] Dev server is running
- [ ] Next.js version is 16+
- [ ] MCP endpoint accessible at `/_next/mcp`
- [ ] Used `nextjs_index` to discover servers
- [ ] Correct port number in `nextjs_call`
- [ ] Git working directory clean (for codemods)
- [ ] Playwright installed (for browser automation)
- [ ] Check both server and client errors
- [ ] Review dev server logs
- [ ] Restart dev server if needed

---

## Getting Help

If still stuck:

1. **Check official documentation:**
   - [Next.js MCP Guide](https://nextjs.org/docs/app/guides/mcp)
   - [next-devtools-mcp GitHub](https://github.com/vercel/next-devtools-mcp)

2. **Review examples:**
   - See `references/examples.md` for complete workflows

3. **Check MCP tools reference:**
   - See `references/mcp-tools-reference.md` for parameters

4. **Community help:**
   - Next.js Discord
   - GitHub Issues on next-devtools-mcp

---

## Error Messages Reference

### ECONNREFUSED
**Meaning:** Cannot connect to dev server
**Fix:** Verify server is running, check port

### 404 at /_next/mcp
**Meaning:** MCP endpoint not available
**Fix:** Upgrade to Next.js 16+

### Tool not available
**Meaning:** Requested tool doesn't exist
**Fix:** Check `nextjs_index` output for available tools

### Git working directory not clean
**Meaning:** Uncommitted changes present
**Fix:** Commit or stash changes before codemods

### Playwright not installed
**Meaning:** Browser automation dependencies missing
**Fix:** Run `npx playwright install`

### Invalid Server Action ID
**Meaning:** Provided ID doesn't match any action
**Fix:** Verify ID format, check if action is exported
