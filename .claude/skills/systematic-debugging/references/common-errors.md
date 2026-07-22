# Common Errors Reference

## JavaScript Errors

### TypeError
```javascript
// Cannot read property 'x' of undefined
const users = undefined;
users.map(u => u.name);  // Error!

// Fix:
(users || []).map(u => u?.name || '');
```

### ReferenceError
```javascript
// variable is not defined
console.log(userName);  // Error if userName not declared

// Fix: Check variable is declared
let userName = 'John';
console.log(userName);
```

### SyntaxError
```javascript
// Unexpected token
if (true {
  console.log('Hello');
}  // Missing )

// Fix: Correct syntax
if (true) {
  console.log('Hello');
}
```

### RangeError
```javascript
// Maximum call stack size exceeded
function recurse() { recurse(); }
recurse();

// Fix: Add termination condition
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}
```

## Async Errors

### Unhandled Promise Rejection
```javascript
// Warning: Unhandled promise rejection
fetch('/api/data').then(data => console.log(data));

// Fix: Add catch
fetch('/api/data')
  .then(data => console.log(data))
  .catch(err => console.error(err));

// Or use async/await with try/catch
async function getData() {
  try {
    const data = await fetch('/api/data');
    return data;
  } catch (err) {
    console.error(err);
  }
}
```

### Cannot read properties of undefined (reading 'then')
```javascript
// Returned value is not a promise
async function bad() {
  return 42;  // Returns 42, not a promise
}
bad().then(...);  // Error!

// Fix: Return promise or use await
async function good() {
  return Promise.resolve(42);
}
```

## React Errors

### Cannot read state of undefined
```javascript
// Class component: 'this' is undefined
class MyComponent extends React.Component {
  handleClick() {
    console.log(this.state.value);  // Error!
  }
  render() {
    return <button onClick={this.handleClick}>Click</button>;
  }
}

// Fix: Bind method or use arrow
class MyComponent extends React.Component {
  handleClick = () => {
    console.log(this.state.value);
  }
}
```

### Too many re-renders
```javascript
// Infinite loop
function MyComponent() {
  setCount(count + 1);  // Triggers re-render
  return <div>{count}</div>;
}

// Fix: Use useEffect for side effects
function MyComponent() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

## Python Errors

### AttributeError
```python
# 'NoneType' object has no attribute 'x'
user = None
print(user.name)  # Error!

# Fix: Check for None
if user:
    print(user.name)
```

### KeyError
```python
# Key not found in dictionary
data = {'name': 'John'}
print(data['age'])  # Error!

# Fix: Use get() or check
print(data.get('age', 'N/A'))
```

### IndentationError
```python
# Inconsistent indentation
def greet():
 print('Hello')  # Error!
    print('World')
```

## Database Errors

### ReferenceError: relation does not exist
```sql
-- Table name might be wrong or migration not run
SELECT * FROM users;

-- Check table exists
SELECT table_name FROM information_schema.tables;
```

### Foreign key violation
```sql
-- Trying to delete referenced row
DELETE FROM users WHERE id = 1;

-- Check dependencies first
SELECT * FROM orders WHERE user_id = 1;
```
