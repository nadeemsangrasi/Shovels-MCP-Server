---
name: nextjs-dev-tool
description: Next.js development tooling via MCP. Inspect routes, components, build info, and debug Next.js apps. Use when working on Next.js 16+ applications, debugging routing issues, inspecting app structure, detecting errors, or testing pages. NOT for general React or non-Next.js projects.
version: 1.0.0
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
author: Claude Code
tags: [nextjs, mcp, debugging, development, routes, inspection, errors, testing, devtools]
---

# Next.js Dev Tool MCP

Debug and inspect Next.js 16+ applications using the official next-devtools-mcp server. Access runtime errors, routes, logs, and application state through Model Context Protocol integration.

## Overview

The Next.js DevTools MCP server connects to your running Next.js dev server's built-in MCP endpoint at `/_next/mcp`, providing real-time inspection, error detection, documentation access, and browser automation for Next.js applications.

## When to Use This Skill

**Activate when:**
- Debugging Next.js 16+ applications
- Inspecting routes and page metadata
- Detecting build or runtime errors
- Testing pages with browser automation
- Querying Next.js documentation
- Upgrading projects to Next.js 16
- Setting up Cache Components
- Investigating Server Actions

**Trigger keywords:** "nextjs debug", "inspect routes", "nextjs errors", "nextjs mcp", "dev tools", "cache components"

**NOT for:**
- General React applications
- Next.js versions below 16 (for runtime tools)
- Production environments
- Static site debugging

## Prerequisites

**Required:**
- Next.js 16+ installed
- Running dev server (`npm run dev`)
- Node.js v20.19+ LTS
- next-devtools-mcp configured in Claude settings

**Optional:**
- Clean git state (for codemods)
- Playwright (auto-installed for browser testing)

## Instructions

### Phase 1: Setup and Discovery

#### Step 1: Initialize DevTools Context

**Run init tool to establish context:**
```typescript
// Sets up Next.js development context
// Documents available MCP tools
```

**See:** `references/mcp-tools-reference.md#init`

#### Step 2: Discover Running Servers

**Use `nextjs_index` to find servers:**
```bash
# Auto-detects servers on ports 3000-3010
# Returns: ports, available tools, project paths
```

**Output includes:**
- Dev server ports
- Available MCP tools per server
- Project locations

**See:** `references/mcp-tools-reference.md#nextjs-index`

### Phase 2: Route and Component Inspection

#### Step 3: Get All Routes

**Via `nextjs_call` with `get_page_metadata`:**
```typescript
// Returns all application routes and pages
```

**Information provided:**
- App Router paths
- Page components
- Layout hierarchy
- Metadata config

**See:** `references/route-inspection.md`

#### Step 4: Get Project Metadata

**Via `get_project_metadata`:**
```typescript
// Returns: structure, config, dev server URL
```

**Use for:**
- Understanding project structure
- Checking configuration
- Verifying dev server status

**See:** `references/examples.md#project-metadata`

### Phase 3: Error Detection

#### Step 5: Check for Errors

**Via `get_errors`:**
```typescript
// Returns: build, runtime, type errors
```

**Detects:**
- Build compilation errors
- Runtime JavaScript errors
- TypeScript type errors
- Hydration mismatches

**See:** `references/error-debugging.md`

#### Step 6: Access Development Logs

**Via `get_logs`:**
```typescript
// Returns path to log file
```

**Then:**
```bash
tail -f /path/to/logs
```

**See:** `references/examples.md#logs`

### Phase 4: Testing and Validation

#### Step 7: Browser Automation Testing

**Via `browser_eval`:**
```typescript
// Actions: start, navigate, screenshot, console_messages, close
```

**Use for:**
- Visual verification
- Console error detection
- User flow testing
- Runtime error capture

**See:** `references/browser-testing.md`

#### Step 8: Server Action Inspection

**Via `get_server_action_by_id`:**
```typescript
// Look up Server Action details by ID
```

**Use when:**
- Debugging forms
- Tracing Server Action calls
- Verifying action bindings

**See:** `references/server-actions.md`

### Phase 5: Documentation Access

#### Step 9: Query Next.js Docs

**Two-step process:**
```typescript
// 1. Search: nextjs_docs action=search, query="middleware"
// 2. Get: nextjs_docs action=get, path from results
```

**Filter options:**
- App Router only
- Pages Router only
- Both routers

**See:** `references/mcp-tools-reference.md#nextjs-docs`

### Phase 6: Upgrades and Migrations

#### Step 10: Upgrade to Next.js 16

**Via `upgrade_nextjs_16`:**
```typescript
// Runs official codemods automatically
```

**Handles:**
- Async API migrations
- Config changes
- Image optimization
- Deprecated API removals

**Requirements:** Clean git state

**See:** `references/upgrade-guide.md`

#### Step 11: Enable Cache Components

**Via `enable_cache_components`:**
```typescript
// Complete automated setup
```

**Process:**
- Pre-flight checks
- Config enablement
- Error detection
- Automated fixes

**See:** `references/cache-components.md`

### Phase 7: Integration with Other Skills

#### Step 12: Use with Authentication Setup

**When using better-auth-nextjs:**
- Verify auth routes with `get_page_metadata`
- Check middleware config
- Test auth flows with `browser_eval`
- Debug hydration in auth components

**See:** `references/integration-guides.md#better-auth`

## Common Patterns

### Pattern 1: Quick Error Check
**Quick:** `nextjs_index` → `nextjs_call` with `get_errors`

**See:** `references/examples.md#error-check`

### Pattern 2: Route Verification
**Quick:** `get_page_metadata` → verify all routes exist

**See:** `references/examples.md#route-check`

### Pattern 3: Full Debug Session
**Quick:** `get_errors` → `get_logs` → `browser_eval` → verify fix

**See:** `references/workflows.md#debug-session`

### Pattern 4: Pre-Deployment Check
**Quick:** Check errors + test routes + browser verification

**See:** `references/workflows.md#pre-deployment`

### Pattern 5: Documentation Lookup
**Quick:** Search docs → get specific page → apply solution

**See:** `references/examples.md#doc-lookup`

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No servers found | Dev server not running | Run `npm run dev` |
| Connection refused | Wrong port | Check `nextjs_index` output |
| Tool not available | Next.js < 16 | Upgrade to 16+ |
| MCP endpoint 404 | Old version | Requires Next.js 16+ |
| Codemod failed | Uncommitted changes | Commit or stash first |

**See:** `references/troubleshooting.md`

## MCP Tools Quick Reference

### Runtime Tools (Require Dev Server)
- **nextjs_index** - Discover servers
- **nextjs_call** - Execute tools
  - get_errors
  - get_logs
  - get_page_metadata
  - get_project_metadata
  - get_server_action_by_id

### Standalone Tools
- **init** - Initialize context
- **nextjs_docs** - Query documentation
- **browser_eval** - Browser automation
- **upgrade_nextjs_16** - Upgrade project
- **enable_cache_components** - Setup caching

**See:** `references/mcp-tools-reference.md`

## Workflow Examples

### Debug Workflow
1. `nextjs_index` - Find servers
2. `get_errors` - Check issues
3. `get_logs` - Review logs
4. `browser_eval` - Test fixes
5. `get_page_metadata` - Verify

**See:** `references/workflows.md#debugging`

### Development Workflow
1. Build features
2. Check routes
3. Test with browser
4. Query docs as needed
5. Verify no errors

**See:** `references/workflows.md#development`

## Best Practices

1. **Always run `nextjs_index` first** - Know what's running
2. **Use `get_errors` frequently** - Catch issues early
3. **Leverage `browser_eval`** - Visual verification matters
4. **Query docs contextually** - Official guidance is best
5. **Test before deploying** - Full checks prevent issues
6. **Keep dev server running** - Required for runtime tools
7. **Use specific MCP tools** - Don't rely only on browser console

## Integration with Other Skills

### With better-auth-nextjs
- Verify auth routes are registered
- Debug middleware conflicts
- Test sign-in/sign-up flows
- Check for hydration errors in auth UI

### With nextjs16
- Verify new features work correctly
- Test routing changes
- Debug App Router issues
- Check metadata configuration

**See:** `references/integration-guides.md`

## Validation Checklist

**Setup:**
- [ ] Next.js 16+ installed
- [ ] Dev server running
- [ ] MCP endpoint accessible
- [ ] next-devtools-mcp configured

**Functionality:**
- [ ] `nextjs_index` discovers servers
- [ ] `get_errors` returns status
- [ ] `get_page_metadata` lists routes
- [ ] `browser_eval` runs tests
- [ ] `nextjs_docs` queries work

## Limitations

- **Next.js 16+ only** for runtime tools
- **Dev server required** for diagnostics
- **Port detection** scans 3000-3010
- **Not for production** debugging
- **Browser automation** needs headless support

## References

**Local Documentation:**
- MCP tools reference: `references/mcp-tools-reference.md`
- Route inspection: `references/route-inspection.md`
- Error debugging: `references/error-debugging.md`
- Browser testing: `references/browser-testing.md`
- Complete examples: `references/examples.md`
- Server Actions: `references/server-actions.md`
- Upgrade guide: `references/upgrade-guide.md`
- Cache Components: `references/cache-components.md`
- Workflows: `references/workflows.md`
- Troubleshooting: `references/troubleshooting.md`
- Integration guides: `references/integration-guides.md`

**External:**
- [GitHub: next-devtools-mcp](https://github.com/vercel/next-devtools-mcp)
- [Next.js MCP Guide](https://nextjs.org/docs/app/guides/mcp)
- [MCP Servers](https://mcpservers.org/servers/vercel/next-devtools-mcp)
- [LobeHub](https://lobehub.com/mcp/vercel-next-devtools-mcp)

## Tips for Success

1. **Keep dev server running** - Most tools need it
2. **Start with `nextjs_index`** - Always discover first
3. **Chain tools effectively** - Detection → fix → verify
4. **Use browser automation** - Don't skip visual checks
5. **Query docs when stuck** - Comprehensive official guides
6. **Test incrementally** - Check after each change
7. **Monitor logs actively** - Watch for warnings
8. **Integrate with skills** - Works great with auth/routing

## Version History

**v1.0.0 (2026-01-01)**
- Initial release
- Next.js 16+ support
- All 7 MCP tools documented
- Runtime diagnostics
- Browser automation
- Upgrade and migration tools
- Integration with existing skills
- Progressive disclosure structure

## Sources

- [GitHub: vercel/next-devtools-mcp](https://github.com/vercel/next-devtools-mcp)
- [Next.js MCP Server Guide](https://nextjs.org/docs/app/guides/mcp)
- [MCP Servers Directory](https://mcpservers.org/servers/vercel/next-devtools-mcp)
- [LobeHub: Next.js DevTools MCP](https://lobehub.com/mcp/vercel-next-devtools-mcp)
