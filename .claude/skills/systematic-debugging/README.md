# Systematic Debugging

A comprehensive Claude Code skill for applying structured debugging methodologies to diagnose and fix software issues efficiently.

## Overview

This skill provides a systematic approach to debugging any software issue, from simple syntax errors to complex distributed system problems. It covers the full debugging lifecycle: reproduction, investigation, isolation, hypothesis, fixing, and prevention.

## Features

### Phase-Based Approach
- **Phase 1:** Reproduce the issue
- **Phase 2:** Gather information
- **Phase 3:** Isolate the problem
- **Phase 4:** Form hypothesis
- **Phase 5:** Fix the issue
- **Phase 6:** Prevent regression

### Debugging Techniques
- Console debugging with advanced logging
- Breakpoint debugging in IDEs
- Network debugging for API issues
- Remote debugging for production
- Database debugging
- Common error patterns

### Tools and Commands
- Chrome DevTools integration
- Node.js debugging with --inspect
- Python PDB debugger
- Git bisect for regression hunting
- Log analysis and filtering

## Installation

```bash
cp -r systematic-debugging /path/to/project/.claude/skills/
```

## Usage

### Activation

Trigger keywords:
- "debug", "fix", "error", "crash", "bug"
- "issue", "troubleshoot", "investigate"
- "not working", "failed", "exception"

### Example Prompts

**Basic Debugging:**
- "Debug this TypeError: Cannot read property"
- "Fix the authentication error"
- "Investigate why tests are failing"

**Advanced Debugging:**
- "Debug race condition in async code"
- "Find the source of memory leak"
- "Debug production issue safely"

## Documentation Structure

```
systematic-debugging/
├── SKILL.md (490 lines)             # Main workflow
├── README.md                         # This file
├── references/
│   ├── console-debugging.md         # Console methods
│   ├── breakpoint-debugging.md      # IDE breakpoints
│   ├── network-debugging.md         # API debugging
│   ├── common-errors.md             # Error reference
│   ├── techniques.md                # Debugging methods
│   └── remote-debugging.md          # Production debugging
├── assets/templates/
└── scripts/
```

## Key Concepts

### The 6-Phase Debugging Process

1. **Reproduce** - Document and consistently reproduce the issue
2. **Gather** - Collect error messages, logs, and stack traces
3. **Isolate** - Narrow down the problem scope
4. **Hypothesis** - Identify root cause through questioning
5. **Fix** - Implement the solution
6. **Prevent** - Add tests and improve error handling

### Error Types

| Type | Example | Solution |
|------|---------|----------|
| SyntaxError | Missing parenthesis | Fix syntax |
| TypeError | Cannot read undefined | Add null checks |
| ReferenceError | Variable not defined | Check imports/variable |
| NetworkError | Request failed | Check API/connectivity |

### Common Techniques

**Rubber Duck Debugging:** Explain code out loud
**Binary Search:** Divide and conquer
**git bisect:** Find regression commits
**Delta Debugging:** Minimal reproduction

## Common Use Cases

### Frontend Issues
- React component errors
- State management bugs
- API integration issues

### Backend Issues
- Database query errors
- Authentication failures
- Performance problems

### Integration Issues
- CORS problems
- Token validation failures
- Service communication errors

## Debugging Checklist

- [ ] Exact error message captured
- [ ] Reproduction steps documented
- [ ] Logs reviewed
- [ ] Root cause identified
- [ ] Fix implemented and tested
- [ ] Tests added to prevent regression
- [ ] Documentation updated

## Tools Covered

**Browsers:**
- Chrome DevTools
- Firefox Developer Tools

**Languages:**
- Node.js (--inspect)
- Python (PDB)
- JavaScript/TypeScript
- Go (Delve)

**Version Control:**
- Git bisect
- Git log analysis

## Requirements

**Knowledge:**
- Programming fundamentals
- Understanding of error types
- Basic command line usage

**Tools:**
- IDE with debugging support
- Browser DevTools
- Access to logs

## Resources

**Local Documentation:**
- Console debugging: `references/console-debugging.md`
- Breakpoint debugging: `references/breakpoint-debugging.md`
- Network debugging: `references/network-debugging.md`
- Techniques: `references/techniques.md`

**External:**
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/)
- [Node.js Debugging](https://nodejs.org/en/docs/guides/debugging-getting-started/)

## Version History

**v1.0.0 (2026-01-01)**
- Initial release
- 6-phase debugging methodology
- Comprehensive error reference
- Multiple debugging techniques
- Progressive disclosure structure (490 lines)

## Tips for Success

1. Start simple, don't overcomplicate
2. Reproduce before fixing
3. Read stack traces carefully
4. Use version control (git bisect)
5. Isolate the problem
6. Question assumptions
7. Take breaks when stuck
8. Rubber duck debugging works!

---

**Created with:** Claude Code + skill-creator
**Documentation Quality:** Production-ready
**Maintenance:** Self-contained, version 1.0.0
