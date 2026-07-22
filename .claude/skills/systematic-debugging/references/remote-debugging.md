# Remote Debugging

## Production Debugging Safely

### Read-Only Investigation
```bash
# View logs without making changes
tail -f /var/log/app.log
grep "ERROR" /var/log/app.log | tail -100

# Check database state (read-only)
SELECT * FROM users WHERE id = 1;
```

### Minimal Impact Debugging
```javascript
// Add temporary debug endpoint
app.get('/debug/state', (req, res) => {
  res.json({
    memory: process.memoryUsage(),
    uptime: process.uptime(),
    environment: process.env.NODE_ENV,
    // Add only what's needed
  });
});
```

## Debugging in Staging

```bash
# Enable debug mode
DEBUG=* npm run start

# Use debug logging
DEBUG=app:*,api:* node app.js

# View debug output
DEBUG=app:* npm run start 2>&1 | tee debug.log
```

## Attaching Debugger Remotely

### Node.js
```bash
# Start with inspector
node --inspect=0.0.0.0:9229 app.js

# Use port forwarding
ssh -L 9229:localhost:9229 user@production-server

# Connect Chrome DevTools: chrome://inspect
```

### Python
```bash
# Start with debug server
python -m debugpy --listen 0.0.0.0:5678 script.py

# Connect from local IDE
# Configure remote debugger to connect to server:5678
```

## Debug Logs in Production

```javascript
// Structured logging
const debugLog = (level, message, data) => {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level,
    message,
    data,
    environment: process.env.NODE_ENV,
  }));
};

// Usage
debugLog('INFO', 'User action', { userId: action.userId });
debugLog('ERROR', 'Failed request', { url: req.url, error: err.message });
```

## Error Tracking Services

### Sentry
```javascript
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: 'https://xxx@sentry.io/xxx',
  environment: process.env.NODE_ENV,
});

// Capture errors
try {
  await riskyOperation();
} catch (err) {
  Sentry.captureException(err);
}
```

### LogRocket
```javascript
import LogRocket from 'logrocket';

LogRocket.init('your-app-id');

// Manual logging
LogRocket.warn('Suspicious activity', { userId });
```

## Health Check Endpoints

```javascript
app.get('/health', async (req, res) => {
  const checks = {
    database: await checkDatabase(),
    memory: process.memoryUsage(),
    uptime: process.uptime(),
  };

  const allHealthy = Object.values(checks).every(c => c.status === 'healthy');

  res.status(allHealthy ? 200 : 503).json({
    status: allHealthy ? 'healthy' : 'unhealthy',
    checks,
  });
});
```

## Debugging Checklist

- [ ] Don't expose sensitive data in debug output
- [ ] Use read-only operations when possible
- [ ] Remove debug endpoints before deployment
- [ ] Log to structured format for easy parsing
- [ ] Set up alerts for errors
- [ ] Use sampling for high-traffic apps
