---
name: docker-containerization
description: Containerize applications with Docker using best practices for Dockerfile optimization, multi-stage builds, docker-compose orchestration, and production deployment. Use when creating Dockerfiles, setting up containers, or configuring multi-container applications.
version: 1.0.0
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
author: Claude Code
tags: [docker, containerization, dockerfile, docker-compose, multi-stage, orchestration, devops, deployment]
---

# Docker Containerization

Containerize applications using Docker with best practices for image optimization, multi-stage builds, and production deployment. Build portable, reproducible, and secure containerized applications.

## Overview

Docker containers provide consistent environments from development to production. This skill covers Dockerfile best practices, multi-stage builds for smaller images, docker-compose for orchestration, and production deployment patterns.

## When to Use This Skill

**Activate when:**
- Creating Dockerfiles
- Setting up containerized applications
- Implementing multi-stage builds
- Configuring docker-compose
- Optimizing container images
- Setting up multi-container applications
- Production deployment with Docker

**Trigger keywords:** "docker", "containerize", "dockerfile", "docker-compose", "multi-stage", "container", "docker hub", "container orchestration"

**NOT for:**
- Kubernetes orchestration (use k8s skill)
- Docker Desktop troubleshooting (general Docker issues)
- Non-containerized deployments

## Prerequisites

**Required:**
- Docker installed and running
- Basic understanding of Linux
- Command line proficiency

**Recommended:**
- Registry account (Docker Hub, ECR, GCR)
- Docker Compose familiarity
- CI/CD knowledge

## Instructions

### Phase 1: Dockerfile Basics

#### Step 1: Create .dockerignore

**Create `.dockerignore`:**
```
node_modules
npm-debug.log
.git
.gitignore
.env
.env.*
Dockerfile
docker-compose.yml
README.md
.vscode
coverage
dist
```

**See:** `references/dockerfile-basics.md#dockerignore`

#### Step 2: Write Basic Dockerfile

**Python/Node.js pattern:**
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

**See:** `references/dockerfile-basics.md#basic`

### Phase 2: Multi-Stage Builds

#### Step 3: Multi-Stage Build Pattern

**Compiled languages (Go/Rust):**
```dockerfile
# Build stage
FROM golang:1.21 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /bin/app

# Production stage
FROM scratch
COPY --from=build /bin/app /bin/app
CMD ["/bin/app"]
```

**Node.js with build step:**
```dockerfile
# Build stage
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

**See:** `references/multi-stage-builds.md`

### Phase 3: Production Optimization

#### Step 4: Layer Caching Optimization

**Order matters - copy dependency files first:**
```dockerfile
FROM node:20-alpine
WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./
RUN npm ci

# Copy source code last
COPY . .
```

**Use --mount=type=cache for package managers:**
```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev
```

**See:** `references/optimization.md#layer-caching`

#### Step 5: Security Best Practices

**Non-root user:**
```dockerfile
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs
USER nodejs
```

**Minimal base images:**
```dockerfile
# Good: Minimal images
FROM node:20-alpine
FROM scratch  # For static binaries

# Avoid: Full images
FROM node:20           # Large
FROM ubuntu:22.04      # Larger
```

**See:** `references/security.md`

### Phase 4: Docker Compose

#### Step 6: Basic Docker Compose

**Create `compose.yaml`:**
```yaml
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://db:5432/app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:

networks:
  default:
    name: app-network
```

**See:** `references/docker-compose.md#basics`

#### Step 7: Environment-Specific Configs

**Development override (`compose.override.yaml`):**
```yaml
services:
  web:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    ports:
      - "3000:3000"
      - "9229:9229"
```

**Production config (`compose.prod.yaml`):**
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
    restart_policy:
      condition: on-failure
      delay: 5s
      max_attempts: 3
```

**See:** `references/docker-compose.md#environments`

### Phase 5: Registry and Deployment

#### Step 8: Build and Push Image

```bash
# Build with tag
docker build -t myapp:latest .

# Tag for registry
docker tag myapp:latest registry.example.com/myapp:v1.0.0

# Push to registry
docker push registry.example.com/myapp:v1.0.0
```

**See:** `references/registry.md`

#### Step 9: Production Deployment

```bash
# Deploy with production config
docker compose -f compose.yaml -f compose.prod.yaml up -d

# Scale services
docker compose up -d --scale web=3
```

**See:** `references/deployment.md`

## Common Patterns

### Pattern 1: Node.js Full Stack
**Quick:** Multi-stage build with frontend build and backend serving

**See:** `references/examples.md#nodejs-fullstack`

### Pattern 2: Python with Gunicorn
**Quick:** Python app with Gunicorn for production

**See:** `references/examples.md#python-gunicorn`

### Pattern 3: Database Container
**Quick:** PostgreSQL/MySQL with volume persistence

**See:** `references/examples.md#database`

### Pattern 4: Multi-Service App
**Quick:** Web + API + Database + Redis

**See:** `references/examples.md#multi-service`

### Pattern 5: Development Environment
**Quick:** Hot reload with volume mounts

**See:** `references/examples.md#development`

## Project Structure Reference

```
project/
├── .dockerignore
├── Dockerfile
├── compose.yaml
├── compose.override.yaml
├── compose.prod.yaml
├── .env.example
├── docker/
│   ├── app/
│   │   └── Dockerfile
│   ├── nginx/
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   └── postgres/
│       └── Dockerfile
└── src/
```

**See:** `references/project-structure.md`

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Connection refused" | Port not exposed | Check EXPOSE and port mapping |
| Layer caching not working | Wrong COPY order | Copy dependency files first |
| Build context too large | .dockerignore missing | Add to .dockerignore |
| Permission denied | Running as root | Create and use non-root user |
| "No such image" | Image not built/pulled | Run docker build/pull |
| Out of memory | Large builds | Use multi-stage, increase Docker memory |

**See:** `references/troubleshooting.md`

## Best Practices Summary

1. **Multi-stage builds** - Smaller production images
2. **Layer ordering** - Dependencies before source code
3. **.dockerignore** - Reduce build context size
4. **Non-root user** - Security best practice
5. **Minimal base images** - Alpine/scratch
6. **Health checks** - Container orchestration
7. **Resource limits** - Prevent resource exhaustion
8. **Environment separation** - Dev vs Prod configs

**See:** `references/best-practices.md`

## Validation Checklist

**Dockerfile:**
- [ ] Multi-stage build for compiled code
- [ ] .dockerignore prevents unnecessary files
- [ ] Non-root user for security
- [ ] Proper layer ordering for caching
- [ ] HEALTHCHECK instruction defined

**Docker Compose:**
- [ ] Environment variables configured
- [ ] Volume mounts for persistence
- [ ] Health checks for dependencies
- [ ] Network isolation between services
- [ ] Resource limits for production

**Security:**
- [ ] No secrets in images
- [ ] Minimal base image
- [ ] Ports not exposed unnecessarily
- [ ] Regular base image updates

## Quick Commands

**Build & Run:**
```bash
docker build -t myapp .
docker run -p 3000:3000 myapp
```

**Docker Compose:**
```bash
docker compose up -d
docker compose logs -f
docker compose down
```

**Cleanup:**
```bash
docker system prune -af
docker image prune -af
```

## References

**Local Documentation:**
- Dockerfile basics: `references/dockerfile-basics.md`
- Multi-stage builds: `references/multi-stage-builds.md`
- Optimization: `references/optimization.md`
- Security: `references/security.md`
- Docker Compose: `references/docker-compose.md`
- Examples: `references/examples.md`
- Troubleshooting: `references/troubleshooting.md`
- Project structure: `references/project-structure.md`

**External Resources:**
- [Docker Official Documentation](https://docs.docker.com)
- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)
- [Docker Compose Reference](https://docs.docker.com/reference/compose-file/)
- [Docker Best Practices](https://docs.docker.com/guides/best-practices/)

## Tips for Success

1. **Start with .dockerignore** - Reduces build context significantly
2. **Use multi-stage builds** - Production images stay small
3. **Test locally first** - `docker compose up -d` before CI/CD
4. **Pin versions** - Use specific tags, not `latest`
5. **Add health checks** - Critical for orchestration
6. **Document ports** - Use EXPOSE instruction
7. **Use Docker Hub** - Explore official images for patterns
8. **CI/CD integration** - Build once, deploy everywhere

## Version History

**v1.0.0 (2026-01-01)** - Initial release with Dockerfile best practices, multi-stage builds, Docker Compose patterns, security guidelines, and Context7 MCP integration

## Sources

- [Docker Official Documentation](https://docs.docker.com)
- [Dockerfile Best Practices](https://docs.docker.com/guides/best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker on Context7](https://context7.com/docker/docs)
