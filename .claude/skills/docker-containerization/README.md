# Docker Containerization

A comprehensive Claude Code skill for containerizing applications using Docker with best practices for Dockerfile optimization, multi-stage builds, docker-compose orchestration, and production deployment.

## Overview

This skill provides guidance on containerizing applications using Docker. It covers Dockerfile best practices, multi-stage builds for optimized images, Docker Compose for multi-container applications, security hardening, and production deployment patterns.

## Features

### Dockerfile Best Practices
- Multi-stage build patterns
- Layer caching optimization
- Non-root user security
- Minimal base image selection
- Build cache mounts

### Docker Compose
- Multi-service orchestration
- Environment-specific configurations
- Health checks and dependencies
- Volume management
- Network configuration

### Production Deployment
- Registry image pushing
- Resource limits
- Restart policies
- Multiple compose files

## Installation

```bash
# Copy to project skills
cp -r docker-containerization /path/to/project/.claude/skills/

# Or copy to global skills
cp -r docker-containerization ~/.claude/skills/
```

## Usage

### Activation

The skill activates with trigger keywords:
- "docker"
- "containerize"
- "dockerfile"
- "docker-compose"
- "multi-stage"
- "container"
- "containerization"

### Example Prompts

**Basic Containerization:**
- "Create a Dockerfile for my Node.js app"
- "Containerize my Python Flask application"
- "Set up multi-stage build for Go application"

**Advanced Patterns:**
- "Create a multi-service application with docker-compose"
- "Set up production deployment with docker-compose"
- "Optimize my Docker image size"

**Security:**
- "Add non-root user to my Dockerfile"
- "Scan my Docker image for vulnerabilities"

## Documentation Structure

```
docker-containerization/
├── SKILL.md (489 lines)              # Main workflow
├── README.md                          # This file
├── references/
│   ├── dockerfile-basics.md          # Dockerfile instructions
│   ├── multi-stage-builds.md         # Multi-stage patterns
│   ├── optimization.md               # Image optimization
│   ├── security.md                   # Security best practices
│   ├── docker-compose.md             # Compose configuration
│   ├── examples.md                   # Complete examples
│   ├── troubleshooting.md            # Common issues
│   └── project-structure.md          # Directory patterns
├── assets/
│   └── templates/
│       ├── Dockerfile-nodejs         # Node.js template
│       ├── Dockerfile-python         # Python template
│       ├── Dockerfile-static         # Static site template
│       ├── compose.yaml              # Base compose
│       ├── .dockerignore             # .dockerignore template
│       └── .env.example              # Environment template
└── scripts/
    └── init-docker.sh                # Project initializer
```

## Key Concepts

### Multi-Stage Builds

Multi-stage builds separate build and runtime environments, producing smaller, more secure production images.

```dockerfile
# Build stage
FROM node:20-alpine AS build
WORKDIR /app
RUN npm ci && npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

### Layer Caching

Docker caches layers from each instruction. Order instructions from least to most frequently changing:

1. Base image
2. Dependency files (package.json, requirements.txt)
3. Install dependencies
4. Application code

### Non-Root Security

Always run containers as non-root users:

```dockerfile
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs
USER nodejs
```

### Docker Compose Patterns

Use multiple compose files for different environments:

```bash
# Development
docker compose up -d

# Production
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

## Common Use Cases

### Node.js API with PostgreSQL

Quick setup with docker-compose, health checks, and volume persistence.

### Python Application with Gunicorn

Production-ready Python container with multi-stage build and non-root user.

### Static Site (React/Vue)

Frontend application served with nginx, minimal production image.

### Full-Stack Application

Multi-container setup with frontend, backend, database, and nginx reverse proxy.

## Integration with Other Skills

### With scaffolding-fastapi
- Containerize FastAPI applications
- Add Docker Compose for dev/prod
- Multi-stage builds for Python

### With styling-with-shadcn
- Containerize Next.js applications
- Multi-stage builds for frontend + API
- Production nginx configuration

### With better-auth-nextjs
- Containerize authenticated applications
- Environment-specific configurations
- Secret management patterns

See `references/examples.md` for detailed workflows.

## Best Practices

1. **Use multi-stage builds** - Smaller production images
2. **Order Dockerfile instructions** - Dependencies before code
3. **Add .dockerignore** - Reduces build context
4. **Run as non-root** - Security best practice
5. **Use Alpine images** - Smaller base images
6. **Add health checks** - Critical for orchestration
7. **Set resource limits** - Prevent resource exhaustion
8. **Separate configs** - Dev vs Prod with compose

## Tools Covered

**Docker:**
- docker build
- docker run
- docker compose
- docker buildx

**Build Optimization:**
- BuildKit
- Build cache mounts
- Multi-stage builds

**Security:**
- Docker Scout
- Trivy
- Non-root users

## Requirements

**Knowledge:**
- Basic Linux commands
- Understanding of processes/ports
- Environment variables

**Tools:**
- Docker installed and running
- Docker Compose (included with Docker Desktop)

## Resources

**Official Documentation:**
- [Docker Documentation](https://docs.docker.com)
- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)
- [Docker Compose Reference](https://docs.docker.com/reference/compose-file/)

**Local Documentation:**
- Dockerfile basics: `references/dockerfile-basics.md`
- Multi-stage builds: `references/multi-stage-builds.md`
- Examples: `references/examples.md`
- Troubleshooting: `references/troubleshooting.md`

## Version History

**v1.0.0 (2026-01-01)**
- Initial release
- Dockerfile best practices
- Multi-stage build patterns
- Docker Compose configuration
- Security hardening
- Production deployment
- Template files and scripts
- Progressive disclosure structure (489 lines)

## Support

- [Docker Community Forums](https://forums.docker.com)
- [Docker GitHub Issues](https://github.com/docker/cli/issues)

## Contributing

Improvements welcome! Please ensure:
- SKILL.md stays under 500 lines
- Examples follow modern best practices
- Templates are production-ready
- References are accurate

---

**Created with:** Claude Code + skill-creator + Context7 MCP
**Documentation Quality:** Production-ready
**Maintenance:** Self-contained, version 1.0.0
