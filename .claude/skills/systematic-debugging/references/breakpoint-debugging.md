# Breakpoint Debugging

## Types of Breakpoints

### Line Breakpoint
Click on line number in IDE/DevTools to pause execution when that line is reached.

### Conditional Breakpoint
```javascript
// In DevTools, right-click breakpoint > Edit
// Condition: userId === null
```

### Logpoint
```javascript
// Right-click breakpoint > Edit
// Log message: "userId is: " + userId
// No pausing
```

### Exception Breakpoint
Pause when exception is thrown (all or caught).

### DOM Breakpoint
Pause when DOM node is modified, removed, or subtree changes.

### Event Breakpoint
Pause when specific event occurs (click, fetch, etc.).

## Debugger Commands

### Step Controls
| Command | Shortcut | Action |
|---------|----------|--------|
| Continue | F8 | Resume execution |
| Step Over | F10 | Execute current line, don't enter functions |
| Step Into | F11 | Enter the function call |
| Step Out | Shift+F11 | Exit current function |
| Restart | Ctrl+Shift+R | Restart debugging session |

## Watch Expressions

```javascript
// Add to watch panel
this.state.users
props.userId
localStorage.getItem('token')
```

## Call Stack Navigation

- Click frames in call stack to see context
- Variables panel shows local variables at each level
- Scope shows: Local, Closure, Global

## Practical Example

```javascript
async function fetchUserData(userId) {
  // Breakpoint here to see userId value
  const response = await fetch(`/api/users/${userId}`);
  // Step over to see response
  const data = await response.json();
  // Step into to see data processing
  return processUserData(data);
}
```

## Remote Debugging Node.js

```bash
# Start with inspector
node --inspect app.js

# Or for TypeScript
node --inspect -r ts-node/register app.ts

# Break on first line
node --inspect-brk app.js
```

Open `chrome://inspect` in Chrome to connect.
