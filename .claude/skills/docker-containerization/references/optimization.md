# Docker Image Optimization

## Layer Caching

Docker caches layers from each instruction. Understanding cache behavior is crucial for fast builds.

### Optimal Instruction Order

```dockerfile
# BAD - Cache invalidates on every code change
FROM node:20-alpine
COPY . .
RUN npm ci
# Rebuilds npm install every time code changes

# GOOD - Dependencies cached separately
FROM node:20-alpine
COPY package*.json ./
RUN npm ci
COPY . .
# npm install only runs when package*.json changes
```

### Minimize Layer Count

```dockerfile
# BAD - Multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y jq
RUN rm -rf /var/lib/apt/lists/*

# GOOD - Single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        jq && \
    rm -rf /var/lib/apt/lists/*
```

### Combine Related Operations

```dockerfile
# Combine cleanup with installation
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git \
        vim \
        && rm -rf /var/lib/apt/lists/*
```

## Build Cache Mounts

Use `--mount=type=cache` to preserve package manager caches between builds.

### npm Cache

```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev
```

### pip Cache

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

### Go Module Cache

```dockerfile
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
```

## Build Context Reduction

### .dockerignore Examples

```
# Exclude development files
node_modules
npm-debug.log
*.log

# Exclude version control
.git
.gitignore

# Exclude IDE
.vscode
.idea

# Exclude docs
README.md
docs/
*.md

# Exclude tests
coverage/
.nyc_output
tests/

# Exclude Docker files
Dockerfile
docker-compose*
.dockerignore
```

### Use Context Wisely

```bash
# Build from subdirectory
docker build -t myapp ./frontend

# Use stdin for context
docker build -t myapp - < Dockerfile
```

## Image Size Reduction

### Use Alpine Base Images

```dockerfile
# Instead of
FROM node:20           # ~1.1 GB
FROM python:3.11       # ~1.0 GB

# Use
FROM node:20-alpine    # ~180 MB
FROM python:3.11-alpine # ~130 MB
```

### Use slim Variants

```dockerfile
FROM python:3.11-slim  # ~140 MB
FROM node:20-slim      # ~300 MB
```

### Multi-Stage for Compiled Languages

```dockerfile
# Build stage (large)
FROM golang:1.21 AS builder
WORKDIR /src
COPY . .
RUN go build -o /app

# Production stage (minimal)
FROM scratch
COPY --from=builder /app /app
CMD ["/app"]
```

### Remove Unnecessary Files

```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        && rm -rf /var/lib/apt/lists/*
```

## BuildKit Features

### Enable BuildKit

```bash
# Using environment variable
DOCKER_BUILDKIT=1 docker build .

# Or use docker buildx
docker buildx build .
```

### Syntax Directive

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine
```

### Secret Mounts

```dockerfile
# Mount secrets without exposing in layers
RUN --mount=type=secret,id=npmrc \
    cat /run/secrets/npmrc > ~/.npmrc && \
    npm ci
```

### SSH Mounts

```dockerfile
# Use SSH for private repos
RUN --mount=type=ssh \
    git clone git@github.com:org/private-repo.git
```

## Common Optimizations

| Optimization | Impact | Example |
|-------------|---------|---------|
| Layer ordering | High | Dependencies before code |
| .dockerignore | Medium | Exclude unnecessary files |
| Alpine images | High | 80% smaller vs full images |
| Multi-stage | High | No build tools in prod |
| Build cache | High | Faster rebuilds |
| Slim variants | Medium | Smaller than full |
| Combine RUN | Low | Fewer layers |
