# Network Debugging

## Network Panel Basics

### Inspecting Requests
1. Open DevTools > Network tab
2. Reload page or perform action
3. Click request to inspect

### Key Columns
- Name: Request URL
- Status: HTTP status code
- Type: MIME type
- Initiator: What triggered request
- Size: Response size
- Time: Duration
- Waterfall: Timeline

## Common Status Codes

| Code | Meaning | Debug Action |
|------|---------|--------------|
| 200 | Success | Check response body |
| 201 | Created | Verify creation |
| 204 | No Content | Check if expected |
| 400 | Bad Request | Validate request |
| 401 | Unauthorized | Check auth token |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Verify URL/ID |
| 500 | Server Error | Check server logs |

## Request Analysis

### Request Headers
```http
GET /api/users/123 HTTP/1.1
Authorization: Bearer eyJ...
Content-Type: application/json
User-Agent: Mozilla/5.0...
```

### Request Payload
```json
{
  "name": "John",
  "email": "john@example.com"
}
```

### Response
```json
{
  "id": 123,
  "name": "John",
  "email": "john@example.com"
}
```

## Debugging Techniques

### Failed Requests
1. Check status code
2. Check Response tab for error message
3. Check server logs

### Slow Requests
1. Check Waterfall column
2. Look for TTFB (Time to First Byte)
3. Check if backend or network issue

### CORS Issues
```
Access to fetch at 'http://localhost:3000' from origin
'http://localhost:8080' has been blocked by CORS policy
```
Fix: Add CORS headers on server

### Request Filtering
- Filter by: domain, method, status, type
- Search: Find specific requests

## Copy as cURL

```bash
# Right-click request > Copy > Copy as cURL
curl 'https://api.example.com/users' \
  -H 'Authorization: Bearer ...' \
  -H 'Content-Type: application/json'
```

## Replay Request
Right-click request > Replay to test with same parameters.
