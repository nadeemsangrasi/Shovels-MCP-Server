# Debugging Techniques

## Rubber Duck Debugging

Explain your code line by line to a rubber duck or colleague. Often you'll find the issue while explaining.

```javascript
// "This function takes a userId, then it calls the API...
// Wait, it doesn't handle the case where userId is undefined..."
```

## Binary Search

Divide code into halves, test each half to find which contains the bug.

```javascript
// Comment out first half
// If bug disappears, bug is in commented code
// If bug remains, bug is in active code
// Repeat with smaller sections
```

## git bisect

Find when a regression was introduced.

```bash
git bisect start
git bisect bad      # Current broken state
git bisect good v1.0.0  # Last known good version

# Test each version
# Mark good or bad
# git bisect will find the commit

git bisect reset  # End session
```

## Delta Debugging

Make minimal changes to isolate the issue.

```javascript
// Original (buggy)
const result = data.users
  .filter(u => u.active)
  .map(u => u.name)
  .sort()
  .join(',');

// Simplify step by step
const result = data.users;  // Bug still here?
const result = users;       // Simplified
```

## Logging Strategically

Add logs at boundaries:

```javascript
console.log('=== ENTER functionName ===');
console.log('Input:', params);

const result = await process(params);

console.log('Output:', result);
console.log('=== EXIT functionName ===');
```

## State Comparison

Compare working vs broken state.

```javascript
// What is different?
const workingUser = { id: 1, name: 'John' };
const brokenUser = { id: 2, name: 'Jane' };

// Check what's different
// - User ID?
// - Database record?
// - Environment variables?
```

## Process of Elimination

1. Does it work in isolation?
2. Does it work with mock data?
3. Does it work in another environment?
4. Does it work with another user?

## Time Travel Debugging

Use tools that record execution:
- Replay recordings
- Step backward through code
- Inspect state at any point

## Snapshot Testing

```javascript
// Before fixing, capture current output
console.log('Current output:', JSON.stringify(output, null, 2));

// After fix, compare
const expected = {...};
expect(output).toEqual(expected);
```

## Test Case Reduction

Create minimal reproduction:

```javascript
// Instead of testing full app
test('handles edge case X', () => {
  // Minimal test case
  const result = process(['X']);
  expect(result).toEqual(['processed X']);
});
```
