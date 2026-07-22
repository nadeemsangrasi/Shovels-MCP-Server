# Docker Compose

## Basic Configuration

### Simple Web App

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
    networks:
      - app-network

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "user", "-d", "app"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

volumes:
  postgres-data:

networks:
  app-network:
    driver: bridge
```

## Service Configuration

### build

```yaml
services:
  web:
    build:
      context: .
      dockerfile: ./docker/Dockerfile
      target: production
      args:
        - BUILD_VERSION=1.0.0
        - NODE_ENV=production
```

### image

```yaml
services:
  web:
    image: registry.example.com/myapp:v1.0.0
    # Or pull from existing image
    image: nginx:alpine
```

### ports

```yaml
services:
  web:
    ports:
      - "3000:3000"           # Host:Container
      - "8080:80"             # Different ports
      - "0.0.0.0:3000:3000"   # Bind to specific interface
```

### environment

```yaml
services:
  web:
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://db:5432/app
      - API_KEY            # Takes value from shell
      - API_KEY=${API_KEY} # Explicit variable
    env_file:
      - .env.production
```

### volumes

```yaml
services:
  web:
    volumes:
      - ./src:/app/src          # Bind mount
      - app-data:/app/data      # Named volume
      - /app/node_modules       # Anonymous volume (persists)
      - type: bind
        source: ./config
        target: /app/config
```

### depends_on

```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy  # Wait for health check
      redis:
        condition: service_started  # Wait for start
```

### networks

```yaml
services:
  web:
    networks:
      - app-network
      - backend-network

networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

### healthcheck

```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
      disable: false
```

## Environment-Specific Configs

### Development Override (compose.override.yaml)

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
      - DEBUG=1
    ports:
      - "3000:3000"
      - "9229:9229"  # Debug port
    stdin_open: true
    tty: true

  db:
    environment:
      - POSTGRES_DB=app_dev
    volumes:
      - ./dev-data:/var/lib/postgresql
```

### Production Config (compose.prod.yaml)

```yaml
services:
  web:
    build:
      target: production
    environment:
      - NODE_ENV=production
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3

  db:
    volumes:
      - postgres-prod:/var/lib/postgresql
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G

volumes:
  postgres-prod:
    driver: local
```

### Using Multiple Files

```bash
# Development (uses override automatically)
docker compose up -d

# Production
docker compose -f compose.yaml -f compose.prod.yaml up -d

# Staging
docker compose -f compose.yaml -f compose.staging.yaml up -d
```

## Complete Example

```yaml
services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://api:8000
    depends_on:
      api:
        condition: service_started

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgres://db:5432/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - frontend
      - api

volumes:
  postgres-data:
  redis-data:

networks:
  default:
    name: app-network
```

## Common Commands

```bash
# Start services
docker compose up -d

# Start with specific config
docker compose -f compose.yaml -f compose.prod.yaml up -d

# View logs
docker compose logs -f
docker compose logs -f web

# Scale services
docker compose up -d --scale web=3

# Stop services
docker compose down
docker compose down -v  # Remove volumes

# Rebuild
docker compose build
docker compose build --no-cache

# Check status
docker compose ps

# Execute command in running container
docker compose exec web sh

# View configuration
docker compose config
```
