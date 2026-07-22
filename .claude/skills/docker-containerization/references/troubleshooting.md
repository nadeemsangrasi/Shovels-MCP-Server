# Docker Troubleshooting

## Build Issues

### "Connection refused" after build

**Cause:** Container running but port not mapped correctly.

**Solution:**
```bash
# Check port mapping
docker ps

# Verify EXPOSE in Dockerfile
EXPOSE 3000

# Map port correctly
docker run -p 3000:3000 myapp
```

### Layer caching not working

**Cause:** COPY order or instruction changes invalidating cache.

**Solution:**
```dockerfile
# BAD - Cache invalidates on every change
COPY . .
RUN npm ci

# GOOD - Dependencies first
COPY package*.json ./
RUN npm ci
COPY . .
```

### "No such image" error

**Cause:** Image not built or pulled.

**Solution:**
```bash
# Build the image
docker build -t myapp .

# Or pull from registry
docker pull myapp:latest

# List available images
docker images
```

### Build context too large

**Cause:** Missing or incomplete .dockerignore.

**Solution:**
```bash
# Check what's in build context
docker context ls
docker build -t myapp . --progress=plain

# Add to .dockerignore
echo "node_modules" >> .dockerignore
echo "*.log" >> .dockerignore
```

### Out of memory during build

**Cause:** Large builds require significant memory.

**Solution:**
```bash
# Increase Docker Desktop memory
# Docker Desktop > Settings > Resources

# Use multi-stage builds
# Build on machine with more RAM

# Use docker buildx with remote builder
docker buildx create --name mybuilder --use
docker buildx build --builder mybuilder .
```

## Runtime Issues

### Permission denied

**Cause:** Running as root or permission issues with volumes.

**Solution:**
```dockerfile
# Add non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup
USER appuser
```

```bash
# Fix volume permissions
docker run -v $(pwd):/app myapp
```

### Container exits immediately

**Cause:** Main process exits or crashes.

**Solution:**
```bash
# Check logs
docker logs myapp
docker logs --tail 100 myapp

# Run interactively
docker run -it myapp sh

# Check entrypoint
docker inspect myapp | grep -i entrypoint
```

### Environment variables not set

**Cause:** Incorrect environment variable syntax.

**Solution:**
```yaml
# docker-compose.yaml
services:
  web:
    environment:
      - NODE_ENV=production  # Correct
      - NODE_ENV production  # Wrong
```

### Database connection failed

**Cause:** Wrong connection string or service not ready.

**Solution:**
```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy  # Wait for health check

  db:
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "user", "-d", "db"]
```

## Docker Compose Issues

### Container won't start

**Cause:** Configuration error or dependency issue.

**Solution:**
```bash
# Validate config
docker compose config

# Check for errors
docker compose up --no-start

# View service status
docker compose ps
```

### Volume not persisting

**Cause:** Named volume not defined or volume removed.

**Solution:**
```yaml
# Define volumes at top level
volumes:
  postgres-data:

# Reference in service
services:
  db:
    volumes:
      - postgres-data:/var/lib/postgresql
```

```bash
# Don't use -v with down (removes volumes)
docker compose down

# To preserve volumes
docker compose down --volumes=false
```

### Port already in use

**Cause:** Another process using the port.

**Solution:**
```bash
# Find process using port
lsof -i :3000

# Or in docker-compose, use different port
ports:
  - "3001:3000"  # Host port 3001 -> Container port 3000
```

### depends_on not waiting

**Cause:** Not using health check condition.

**Solution:**
```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy  # Wait for health check

  db:
    healthcheck:
      test: ["CMD", "pg_isready"]
```

## Network Issues

### Can't connect between containers

**Cause:** Containers on different networks.

**Solution:**
```yaml
services:
  web:
    networks:
      - app-network
  db:
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### DNS resolution failed

**Cause:** Network configuration or service name issue.

**Solution:**
```bash
# Check network
docker network ls
docker network inspect app-network

# Use service name for connection
# postgres://db:5432/app (db is service name)
```

## Performance Issues

### Slow builds

**Solution:**
```bash
# Use BuildKit
DOCKER_BUILDKIT=1 docker build .

# Enable BuildKit by default
export DOCKER_BUILDKIT=1

# Use cache mounts
RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

### Large image sizes

**Solution:**
```dockerfile
# Use multi-stage builds
FROM node:20-alpine AS build
# ... build steps ...
FROM node:20-alpine AS production
COPY --from=build /app/dist /app/dist

# Use Alpine
FROM node:20-alpine

# Don't include unnecessary files
COPY package*.json ./
RUN npm ci --omit=dev
```

### Container runs slow

**Solution:**
```yaml
# Limit resources
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

## Security Issues

### Vulnerabilities in image

**Solution:**
```bash
# Scan with Trivy
trivy image myapp:latest

# Scan with Docker Scout
docker scout quickview myapp:latest

# Update base image
docker pull node:20-alpine
```

### Secrets in image

**Solution:**
```dockerfile
# Don't COPY secrets
# COPY ./secrets /app/secrets  # BAD

# Use build arguments
ARG API_KEY
ENV API_KEY=${API_KEY}

# Use runtime secrets
RUN --mount=type=secret,id=npmrc \
    cat /run/secrets/npmrc > ~/.npmrc
```

## Useful Commands

```bash
# View logs
docker logs -f myapp

# Inspect container
docker inspect myapp

# Check container stats
docker stats myapp

# View network
docker network ls
docker network inspect network-name

# Prune everything
docker system prune -af
docker image prune -af
docker builder prune -af

# Debug with shell
docker run -it myapp sh
docker compose exec web sh
```
