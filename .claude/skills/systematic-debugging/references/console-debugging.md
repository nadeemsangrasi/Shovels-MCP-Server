# Console Debugging

## Console Methods

```javascript
// Basic logging
console.log('Message');          // Info
console.info('Info message');    // Info
console.warn('Warning');         // Warning
console.error('Error');          // Error

// Grouping
console.group('Operation');
console.log('Step 1');
console.log('Step 2');
console.groupEnd();

// Table
console.table([{name: 'John', age: 30}, {name: 'Jane', age: 25}]);

// Timing
console.time('operation');
// ... code
console.timeEnd('operation');

// Stack trace
console.trace();

// Assert
console.assert(condition, 'This should be true');
```

## Advanced Techniques

### Object Inspection
```javascript
// Full object inspection
console.log('Data:', data);
console.log('Data %o', data);

// With formatting
console.log('User: %s, ID: %d', user.name, user.id);
```

### Color Coding
```javascript
console.log('%cCustom styling', 'color: red; font-size: 20px;');
console.log('%cSuccess', 'color: green', result);
console.log('%cError', 'color: red', error);
```

## Performance Logging
```javascript
const logPerformance = (name, fn) => {
  console.time(name);
  const result = fn();
  console.timeEnd(name);
  return result;
};
```

## Filtering Logs
```javascript
// In browser console
// Filter by: error, warning, info

// Programmatic filtering
const logger = (level, message) => {
  if (level === 'error') {
    console.error(message);
  }
};
```
