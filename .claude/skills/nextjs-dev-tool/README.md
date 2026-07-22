# Next.js Dev Tool MCP

Debug and inspect Next.js 16+ applications using the official next-devtools-mcp server through Model Context Protocol.

## Overview

This skill provides comprehensive Next.js development tools including route inspection, error detection, browser automation, documentation access, and project upgrades—all integrated through MCP.

## Features

### Runtime Diagnostics
- ✅ Error detection (build, runtime, type errors)
- ✅ Route inspection and metadata
- ✅ Development logs access
- ✅ Project metadata and configuration
- ✅ Server Action debugging

### Testing and Automation
- ✅ Browser automation with Playwright
- ✅ Visual regression testing
- ✅ Console error capture
- ✅ User flow testing

### Documentation and Help
- ✅ Next.js documentation search
- ✅ API reference lookup
- ✅ Context-aware guidance

### Project Management
- ✅ Automated upgrade to Next.js 16
- ✅ Cache Components setup
- ✅ Codemod execution

### Integration
- ✅ Works with better-auth-nextjs skill
- ✅ Complements nextjs16 skill
- ✅ Integrates with development workflow

## Installation

### Prerequisites

1. **Next.js 16+** installed in your project:
   ```bash
   npm install next@latest
   ```

2. **next-devtools-mcp** configured in Claude settings:
   ```json
   {
     "mcpServers": {
       "nextjs-devtools": {
         "command": "npx",
         "args": ["-y", "next-devtools-mcp"]
       }
     }
   }
   ```

### Skill Installation

```bash
# Copy to project skills
cp -r nextjs-dev-tool /path/to/project/.claude/skills/

# Or copy to global skills
cp -r nextjs-dev-tool ~/.claude/skills/
```

## Usage

### Activation

The skill activates with trigger keywords:
- "nextjs debug"
- "inspect routes"
- "nextjs errors"
- "nextjs mcp"
- "dev tools"
- "cache components"

### Basic Workflow

```bash
# 1. Start your Next.js dev server
npm run dev

# 2. Use Claude Code with trigger keywords
"Check for errors in my Next.js app"
"Inspect all routes"
"Test my sign-in page"
"Upgrade to Next.js 16"
```

### Example Prompts

**Error Detection:**
- "Check if there are any errors in my Next.js app"
- "Show me all build and runtime errors"
- "Get the development logs"

**Route Inspection:**
- "List all routes in my application"
- "Inspect the /dashboard route"
- "Verify my auth routes are registered"

**Browser Testing:**
- "Test the sign-in page and check for errors"
- "Take a screenshot of the homepage"
- "Test the checkout flow"

**Documentation:**
- "Look up Next.js middleware documentation"
- "Find information about generateMetadata"
- "Search for Cache Components setup"

**Upgrades:**
- "Upgrade my project to Next.js 16"
- "Enable Cache Components"

## Documentation Structure

```
nextjs-dev-tool/
├── SKILL.md (412 lines)             # Main skill workflow
├── README.md                         # This file
├── references/
│   ├── mcp-tools-reference.md        # Complete tool documentation
│   ├── examples.md                   # Full workflow examples
│   ├── troubleshooting.md            # Common issues and fixes
│   └── integration-guides.md         # Integration with other skills
└── scripts/
    └── check-nextjs-version.sh       # Version validation script
```

## MCP Tools Available

### Runtime Diagnostic Tools
- **nextjs_index** - Discover running servers
- **nextjs_call** - Execute diagnostic tools
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

## Common Use Cases

### Debug Session
1. Discover servers → Check errors → Review logs → Test fix

### Route Verification
1. Get all routes → Verify expected routes → Test in browser

### Pre-Deployment
1. Check errors → Test critical pages → Take screenshots → Verify

### Authentication Setup
1. Verify auth routes → Test sign-in → Check middleware → Test protected routes

### Project Upgrade
1. Backup code → Run upgrade tool → Fix issues → Test thoroughly

## Integration with Other Skills

### With better-auth-nextjs
- Verify auth routes after setup
- Test authentication flows
- Debug hydration errors
- Check middleware configuration

### With nextjs16
- Verify new features work
- Test routing changes
- Debug App Router issues
- Check metadata configuration

See `references/integration-guides.md` for complete workflows.

## Requirements

**Minimum:**
- Next.js 16.0.0 or higher
- Node.js v20.19+ LTS
- Running dev server

**Optional:**
- Playwright (auto-installed)
- Clean git state (for codemods)

## Limitations

- **Next.js 16+ only** for runtime diagnostic tools
- **Dev server required** for most features
- **Development only** - not for production debugging
- **Port detection** scans 3000-3010
- **Browser automation** needs headless browser support

## Troubleshooting

### No Servers Found
**Solution:** Ensure dev server is running with `npm run dev`

### Connection Refused
**Solution:** Run `nextjs_index` to get correct port

### Tool Not Available
**Solution:** Upgrade to Next.js 16+

### MCP Endpoint 404
**Solution:** Requires Next.js 16+ (MCP built-in)

See `references/troubleshooting.md` for complete guide.

## Best Practices

1. **Always run `nextjs_index` first** - Know what's running
2. **Use `get_errors` frequently** - Catch issues early
3. **Leverage browser automation** - Visual verification is crucial
4. **Query docs contextually** - Official guidance is comprehensive
5. **Test incrementally** - Verify after each change
6. **Keep dev server running** - Required for most tools
7. **Integrate with other skills** - Works great with auth and routing

## Resources

**Official:**
- [GitHub: next-devtools-mcp](https://github.com/vercel/next-devtools-mcp)
- [Next.js MCP Guide](https://nextjs.org/docs/app/guides/mcp)
- [MCP Servers Directory](https://mcpservers.org/servers/vercel/next-devtools-mcp)

**Local Documentation:**
- Complete tool reference: `references/mcp-tools-reference.md`
- Full examples: `references/examples.md`
- Troubleshooting: `references/troubleshooting.md`
- Integration guides: `references/integration-guides.md`

## Version History

**v1.0.0 (2026-01-01)**
- Initial release
- Next.js 16+ support
- All 7 MCP tools documented
- Runtime diagnostics
- Browser automation
- Upgrade and migration tools
- Integration with existing skills
- Progressive disclosure structure (412 lines)

## Support

- Next.js Discord
- [GitHub Issues](https://github.com/vercel/next-devtools-mcp/issues)
- Claude Code community

## License

This skill integrates with:
- next-devtools-mcp (MIT License)
- Next.js (MIT License)
- Playwright (Apache 2.0 License)

## Contributing

Improvements welcome! Please ensure:
- SKILL.md stays under 500 lines
- Examples are tested
- Documentation is clear
- Integration guides are updated

---

**Created with:** Claude Code + skill-creator + research
**Documentation Quality:** Production-ready
**Maintenance:** Self-contained, version 1.0.0
