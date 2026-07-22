# Dockerfile Basics

## .dockerignore

The `.dockerignore` file prevents unnecessary files from being copied into the build context, reducing image size and build time.

### Essential Patterns

```
# Version control
.git
.gitignore
.gitattributes

# Dependencies
node_modules
venv
.env
.env.local
.env.*.local

# Build output
dist
build
*.log
npm-debug.log
yarn-debug.log
yarn-error.log

# IDE
.vscode
.idea
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
Dockerfile
docker-compose.yml
docker-compose.override.yml

# Documentation
README.md
CHANGELOG.md
LICENSE

# Tests
coverage
.nyc_output
*.lcov

# CI/CD
.github
.gitlab-ci.yml
.travis.yml
Jenkinsfile
```

### Examples

**Node.js project:**
```
node_modules
npm-debug.log
.git
.gitignore
.env
.env.local
dist
coverage
.vscode
Dockerfile
docker-compose.yml
README.md
```

**Python project:**
```
venv
__pycache__
*.pyc
*.pyo
*.egg-info
.eggs
dist
build
*.log
.env
.git
.gitignore
Dockerfile
docker-compose.yml
```

**Go project:**
```
.git
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
go.work
```

## Basic Dockerfile Instructions

### FROM

Sets the base image for subsequent instructions.

```dockerfile
# Official images
FROM node:20-alpine
FROM python:3.11-slim
FROM golang:1.21

# Multi-platform
FROM --platform=$BUILDPLATFORM node:20-alpine AS builder

# Scratch (minimal - for static binaries)
FROM scratch
```

### WORKDIR

Sets the working directory for any RUN, CMD, ENTRYPOINT, COPY, or ADD instructions.

```dockerfile
WORKDIR /app
WORKDIR /usr/src/app
WORKDIR ${APP_DIR:-/app}
```

### COPY

Copies new files or directories from the build context.

```dockerfile
# Copy single file
COPY package.json ./

# Copy with glob pattern
COPY package*.json ./

# Copy directory contents
COPY src ./src

# Copy with ownership
COPY --chown=nodejs:nodejs . .
```

### ADD

Similar to COPY but with additional features (remote URLs, auto-extraction).

```dockerfile
# Use COPY for local files (preferred)
COPY ./file.txt /app/file.txt

# Use ADD only for URLs or tar extraction
ADD https://example.com/file.tar.gz /app/
ADD file.tar.gz /app/  # Auto-extracts
```

### RUN

Executes any command in a new layer.

```dockerfile
# Shell form
RUN npm ci

# Exec form (preferred)
RUN ["npm", "ci"]

# With cache mount for package managers
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# With security (non-root)
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup
```

### EXPOSE

Documents the port the container listens on.

```dockerfile
EXPOSE 3000
EXPOSE 80/tcp
EXPOSE 443/ssl
EXPOSE 3000 8080
```

### ENV

Sets environment variables.

```dockerfile
ENV NODE_ENV=production
ENV APP_PORT=3000
ENV PATH=/app/node_modules/.bin:$PATH
```

### CMD

Provides defaults for an executing container.

```dockerfile
# Exec form (preferred)
CMD ["node", "server.js"]

# Shell form
CMD node server.js

# With parameters
CMD ["npm", "start"]
```

### ENTRYPOINT

Configures a container to run as an executable.

```dockerfile
# Exec form
ENTRYPOINT ["npm", "start"]

# Can be overridden with --entrypoint
docker run --entrypoint /bin/sh myapp
```

## Quick Reference

| Instruction | Purpose | Example |
|------------|---------|---------|
| FROM | Base image | `FROM node:20-alpine` |
| WORKDIR | Working directory | `WORKDIR /app` |
| COPY | Copy files | `COPY . .` |
| RUN | Execute command | `RUN npm ci` |
| EXPOSE | Document ports | `EXPOSE 3000` |
| ENV | Environment vars | `ENV NODE_ENV=prod` |
| CMD | Default command | `CMD ["node"]` |
| ENTRYPOINT | Executable | `ENTRYPOINT ["node"]` |
