# Docker Security Best Practices

## Run as Non-Root User

Running containers as root is a major security risk. Always create and use a non-root user.

### Node.js

```dockerfile
FROM node:20-alpine

# Create group and user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs

WORKDIR /app

# Set ownership
COPY --chown=nodejs:nodejs package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

COPY --chown=nodejs:nodejs . .

USER nodejs

CMD ["node", "server.js"]
```

### Python

```dockerfile
FROM python:3.11-slim

# Create non-root user
RUN groupadd --system --gid 1001 appgroup && \
    useradd --system --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy and set ownership
COPY --chown=appuser:appgroup requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup . .

USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Go (scratch image)

```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app

# Use scratch - no user needed (no user exists in scratch)
FROM scratch
COPY --from=builder /app /app
CMD ["/app"]
```

## Avoid Sensitive Data in Images

### Don't COPY secrets

```dockerfile
# BAD
COPY ./secrets/api-key.json /app/secrets/

# GOOD - Use runtime environment
ENV API_KEY_FILE=/run/secrets/api-key
```

### Use Docker secrets (Docker Swarm)

```yaml
services:
  app:
    secrets:
      - api_key
    environment:
      - API_KEY_FILE=/run/secrets/api_key

secrets:
  api_key:
    file: ./secrets/api-key.txt
```

### Use BuildKit secrets

```dockerfile
RUN --mount=type=secret,id=npmrc \
    cat /run/secrets/npmrc > ~/.npmrc && \
    npm ci
```

## Minimal Base Images

### Image Size Comparison

| Image | Size | Use Case |
|-------|------|----------|
| `node:20` | ~1.1 GB | Full development |
| `node:20-slim` | ~300 MB | Minimal runtime |
| `node:20-alpine` | ~180 MB | Smallest (recommended) |
| `scratch` | ~0 MB | Static binaries only |

### Alpine Considerations

Alpine uses musl libc instead of glibc. Some applications may need glibc:

```dockerfile
# For Node.js - use official Alpine
FROM node:20-alpine

# For Go binaries compiled with glibc
FROM gcr.io/distroless/static-debian12
```

## Scan Images for Vulnerabilities

### Use trivy

```bash
# Install trivy
brew install trivy

# Scan image
trivy image myapp:latest

# Scan Dockerfile
trivy config .
```

### Use docker scout

```bash
# Enable Docker Scout
docker scout enable

# Quick overview
docker scout quickview myapp:latest

# Detailed report
docker scout cves myapp:latest
```

## Limit Capabilities

### Drop all capabilities, add only what's needed

```dockerfile
# Start with no privileges
FROM node:20-alpine
RUN adduser --system --disabled-password appuser

# For specific capabilities (example: binding to port < 1024)
# NET_BIND_SERVICE capability allows binding to privileged ports
```

### Security profiles with Docker

```bash
# Run with security profile
docker run --security-opt seccomp=profile.json myapp
docker run --security-opt apparmor=profile-name myapp
```

## Read-Only Root Filesystem

```bash
docker run --read-only myapp
```

For directories that need write access:

```bash
docker run --read-only -v /tmp myapp
```

## No New Privileges

```bash
docker run --security-opt=no-new-privileges myapp
```

## Health Checks

Health checks help orchestration know when to restart containers:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"
```

### Docker Compose health check

```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

## Resource Limits

### Memory

```bash
docker run -m 512m myapp
```

### CPU

```bash
docker run --cpus=1.5 myapp
docker run --cpuset-cpus="0,1" myapp
```

### Docker Compose

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## Regular Updates

Keep base images updated for security patches:

```bash
# Pull latest
docker pull node:20-alpine

# Use renovate bot for automated updates
```

## Security Checklist

- [ ] Run as non-root user
- [ ] No secrets in images
- [ ] Use minimal base images
- [ ] Regular vulnerability scans
- [ ] Health checks defined
- [ ] Resource limits set
- [ ] Read-only filesystem where possible
- [ ] No new privileges flag
- [ ] .dockerignore prevents sensitive files
