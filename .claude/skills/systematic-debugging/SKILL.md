---
name: systematic-debugging
description: Apply systematic debugging methodologies to diagnose and fix software issues. Use when encountering bugs, crashes, errors, or unexpected behavior. Covers error analysis, logging strategies, breakpoint debugging, and root cause identification.
version: 1.0.0
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
author: Claude Code
tags: [debugging, troubleshooting, error-fixing, diagnostics, logging, breakpoints, root-cause, investigation, bug-fixing, testing]
---

# Systematic Debugging

Apply structured debugging methodologies to diagnose and fix software issues efficiently. Develop systematic problem-solving skills for any codebase.

## Overview

Debugging is a systematic process of identifying, isolating, and fixing bugs. This skill provides frameworks for approaching any debugging scenario, from simple syntax errors to complex distributed system issues.

## When to Use This Skill

**Activate when:**
- Encountering errors or crashes
- Application behaves unexpectedly
- Tests are failing
- API returns unexpected responses
- Performance issues arise
- Security vulnerabilities discovered

**Trigger keywords:** "debug", "fix", "error", "crash", "bug", "issue", "troubleshoot", "investigate", "not working", "failed", "exception"

**NOT for:**
- Code writing from scratch
- Performance optimization without profiling
- Security penetration testing

## Prerequisites

**Required:**
- Access to codebase
- Understanding of the technology stack
- Patience and systematic approach

**Recommended:**
- IDE with debugging capabilities
- Log access
- Test suite

## Instructions

### Phase 1: Reproduce the Issue

#### Step 1: Document the Symptom

**Record what you observe:**
- Error messages (exact text)
- Expected behavior vs actual
- Steps to reproduce
- Environment details (OS, versions)
- Frequency (always, sometimes, once)

**Example:**
```
Error: Cannot read property 'map' of undefined
Location: UserList.tsx:42
Steps: Navigate to /users, click on any user
Expected: Show user details
Actual: White screen, console error
```

#### Step 2: Reproduce Consistently

**Minimize variables:**
```bash
# Isolate the issue
npm test -- --testNamePattern="user list"
# Run with clean state
rm -rf node_modules && npm install
# Test in incognito/private window
```

**Check reproduction rate:**
- Does it happen every time?
- Does it happen on different browsers?
- Does it happen on different environments?

### Phase 2: Gather Information

#### Step 3: Read Error Messages Carefully

**Parse the error:**
```javascript
// TypeError: Cannot read property 'map' of undefined
//    ^     ^                                ^
//    |     |                                └── What's wrong (undefined)
//    |     └── What operation (reading property)
//    └── What type (TypeError)
```

**Extract key information:**
- Error type (TypeError, ReferenceError, SyntaxError)
- Message (what went wrong)
- Stack trace (where it happened)
- Line number (exact location)

#### Step 4: Check Logs

**Application logs:**
```bash
# View logs
tail -f logs/app.log

# Filter for errors
grep -i error logs/app.log

# Check specific time range
awk '/2024-01-15/ && /10:00/,/11:00/' logs/app.log
```

**Browser console:**
```javascript
// Enable verbose logging
localStorage.debug = '*'

// Check network requests
// Look at failed requests (red in Network tab)
```

**Database logs:**
```sql
-- Check for errors
SELECT * FROM logs WHERE level = 'error' ORDER BY created_at DESC LIMIT 100;
```

#### Step 5: Add Strategic Logging

**Minimal logging to understand flow:**
```javascript
console.log('ENTER: fetchUsers');
console.log('userId:', userId);
console.log('BEFORE: API call');
const users = await api.getUsers(userId);
console.log('AFTER: API call, users:', users?.length);
console.log('EXIT: fetchUsers');
```

**State inspection:**
```javascript
// Before the error
console.log('Component state:', {
  users: state.users,
  loading: state.loading,
  error: state.error
});
```

### Phase 3: Isolate the Problem

#### Step 6: Narrow Down Scope

**Binary search approach:**
```
Is the issue in frontend or backend?
├─ Test API directly → If works, issue is frontend
└─ If fails, issue is backend

Is the issue in a specific component?
├─ Remove components one by one
└─ Add back until issue reappears
```

**Comment out code:**
```javascript
// // Temporarily disable
// async function fetchUsers() {
//   const users = await api.getUsers(userId);
//   return users;
// }

// Simpler version to test
const users = [];
renderUsers(users);
```

#### Step 7: Check Related Components

**Dependencies:**
```javascript
// Is the data structure correct?
console.log('API response:', response);
console.log('Expected shape:', { users: [] });

// Are required libraries loaded?
if (typeof lodash !== 'undefined') {
  console.log('Lodash loaded');
} else {
  console.log('Lodash NOT loaded');
}
```

**Environment:**
```javascript
// Check environment variables
console.log('API_URL:', process.env.API_URL);
console.log('NODE_ENV:', process.env.NODE_ENV);
```

### Phase 4: Form Hypothesis

#### Step 8: Identify Root Cause

**Ask "why" repeatedly:**
```
Why is users undefined?
→ Because API returned null
Why did API return null?
→ Because userId is invalid
Why is userId invalid?
→ Because route param wasn't parsed
```

**Common root causes:**
- Undefined/null values passed
- Incorrect data types
- Missing required parameters
- Race conditions
- Async timing issues
- Environment misconfiguration

#### Step 9: Verify Hypothesis

**Test the theory:**
```javascript
// Hypothesis: userId is undefined
console.log('Testing hypothesis - userId:', userId);

// If confirmed, find where it should come from
// Check route params
console.log('Route params:', params);
```

**Create a test case:**
```javascript
test('handles missing userId gracefully', async () => {
  const result = await fetchUsers(undefined);
  expect(result).toEqual([]);
});
```

### Phase 5: Fix the Issue

#### Step 10: Implement the Fix

**Defensive coding:**
```javascript
// Before (fragile)
users.map(u => u.name);

// After (defensive)
(users || []).map(u => u?.name || '');
```

**Add validation:**
```javascript
async function fetchUsers(userId) {
  if (!userId) {
    console.warn('fetchUsers called without userId');
    return [];
  }
  // ... rest of function
}
```

#### Step 11: Verify the Fix

**Test the fix:**
```bash
# Run the reproduction steps
npm test -- --testNamePattern="user list"

# Check if error still occurs
# Verify expected behavior
```

**Check related functionality:**
```bash
# Run full test suite
npm test

# Check for regressions
# Verify edge cases
```

### Phase 6: Prevent Regression

#### Step 12: Add Tests

**Unit test:**
```javascript
test('fetchUsers handles undefined userId', async () => {
  const result = await fetchUsers(undefined);
  expect(result).toEqual([]);
});
```

**Integration test:**
```javascript
test('UserList displays empty state when no users', async () => {
  render(<UserList userId="invalid" />);
  expect(screen.getByText('No users found')).toBeInTheDocument();
});
```

#### Step 13: Improve Error Handling

**Better error messages:**
```javascript
if (!users) {
  throw new Error(`Failed for userId: ${userId}. Response: ${JSON.stringify(response)}`);
}
```

## Common Debugging Patterns

### Pattern 1: Console Debugging
**Quick:** Strategic console.log statements

**See:** `references/console-debugging.md`

### Pattern 2: Breakpoint Debugging
**Quick:** IDE breakpoints and step-through

**See:** `references/breakpoint-debugging.md`

### Pattern 3: Network Debugging
**Quick:** Inspect API calls and responses

**See:** `references/network-debugging.md`

### Pattern 4: Remote Debugging
**Quick:** Debug production issues safely

**See:** `references/remote-debugging.md`

## Quick Reference

### Error Types

| Type | Cause | Solution |
|------|-------|----------|
| SyntaxError | Invalid code syntax | Fix syntax, check parentheses/braces |
| ReferenceError | Undefined variable | Check variable name, imports |
| TypeError | Wrong type operation | Check data types, add null checks |
| RangeError | Value out of range | Check array bounds, recursion |
| NetworkError | Request failed | Check API, network connectivity |

### Debugging Commands

```bash
# Node.js
node --inspect app.js        # Start with debugger
node --trace-warnings app.js # Trace warnings

# Browser
# Open DevTools > Sources > Add breakpoints

# Python
python -m pdb script.py       # PDB debugger
python -c "import pdb; pdb.pm()"  # Post-mortem

# Database
EXPLAIN ANALYZE your_query;   # Query analysis
```

## Error Handling Checklist

- [ ] Error message captured and documented
- [ ] Steps to reproduce documented
- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Fix tested
- [ ] Tests added
- [ ] Similar issues checked

## Best Practices

1. **Start simple** - Check obvious causes first
2. **Reproduce first** - Can't fix what you can't reproduce
3. **Read stack traces** - They contain valuable information
4. **Use version control** - `git bisect` for regression hunting
5. **Isolate the problem** - Divide and conquer
6. **Question assumptions** - What you think is true might not be
7. **Document findings** - Write down what you learned
8. **Automate reproduction** - Create failing tests

## Validation Checklist

**Issue Reproduction:**
- [ ] Exact error message captured
- [ ] Reproduction steps documented
- [ ] Issue reproduced consistently

**Investigation:**
- [ ] Logs reviewed
- [ ] Stack trace analyzed
- [ ] Root cause identified

**Fix:**
- [ ] Fix implemented
- [ ] Fix tested
- [ ] No regressions

**Prevention:**
- [ ] Tests added
- [ ] Error handling improved
- [ ] Documentation updated

## Quick Commands

**Debug Node.js:**
```bash
node --inspect app.js
# Open chrome://inspect in Chrome
```

**Debug Python:**
```bash
python -m pdb script.py
# (pdb) n (next), (pdb) s (step), (pdb) c (continue)
```

**Debug in browser:**
```javascript
// Add breakpoint
debugger;

// Or in DevTools Sources tab
// Click line number to add breakpoint
```

**Git bisect (find regression):**
```bash
git bisect start
git bisect bad  # Current broken version
git bisect good v1.0.0  # Last known good
# Git will checkout versions for testing
git bisect reset  # End session
```

## References

**Local Documentation:**
- Console debugging: `references/console-debugging.md`
- Breakpoint debugging: `references/breakpoint-debugging.md`
- Remote debugging: `references/remote-debugging.md`
- Network debugging: `references/network-debugging.md`
- Database debugging: `references/database-debugging.md`
- Common errors: `references/common-errors.md`
- Techniques: `references/techniques.md`

**External Resources:**
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/)
- [Node.js Debugging](https://nodejs.org/en/docs/guides/debugging-getting-started/)
- [Python PDB](https://docs.python.org/3/library/pdb.html)

## Tips for Success

1. **Take breaks** - Fresh eyes catch more
2. **Rubber duck** - Explain the problem out loud
3. **Search effectively** - Copy exact error message
4. **Check docs** - Read error message, then docs
5. **Ask for help** - After trying systematically
6. **Document everything** - Future you will thank you
7. **Learn patterns** - Similar issues have similar fixes

## Version History

**v1.0.0 (2026-01-01)** - Initial release with systematic debugging methodology, 6-phase approach (reproduce, gather, isolate, hypothesize, fix, prevent), debugging patterns, and reference guides

## Sources

- Chrome DevTools Documentation
- Node.js Debugging Guide
- Python PDB Documentation
- Debugging textbooks and best practices
