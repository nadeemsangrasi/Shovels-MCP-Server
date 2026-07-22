# Docker Examples

## Node.js Full Stack

### Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
ARG NODE_VERSION=20-alpine

FROM node:${NODE_VERSION} AS base
WORKDIR /app

FROM base AS deps
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev

FROM base AS build
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS production
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY --from=build /app/package.json ./
USER nodejs
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### compose.yaml

```yaml
services:
  web:
    build:
      context: .
      target: production
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
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "app", "-d", "app"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:
```

## Python with Gunicorn

### Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base
WORKDIR /app

FROM base AS deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY --from=deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
RUN groupadd --system --gid 1001 appgroup && \
    useradd --system --uid 1001 --gid appgroup appuser
RUN chown -R appuser:appgroup /app
USER appuser
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
```

### compose.yaml

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgres://db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  worker:
    build: .
    command: celery -A app worker
    environment:
      - DATABASE_URL=postgres://db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

volumes:
  static-files:
```

## Database Container

### PostgreSQL with Init Scripts

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql
      - ./init-scripts:/docker-entrypoint-initdb.d
      - ./schema.sql:/docker-entrypoint-initdb.d/01-schema.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app"]
      interval: 10s
      timeout: 5s
      retries: 5
    ports:
      - "5432:5432"  # Only for development!

volumes:
  postgres-data:
```

### MySQL

```yaml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${ROOT_PASSWORD}
      MYSQL_DATABASE: app
      MYSQL_USER: app
      MYSQL_PASSWORD: ${APP_PASSWORD}
    volumes:
      - mysql-data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  mysql-data:
```

## Multi-Service Application

```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      api:
        condition: service_started

  api:
    build: ./backend
    ports:
      - "8000:8000"
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
      test: ["CMD", "pg_isready", "-U", "app", "-d", "app"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
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

## Development Environment

### Dockerfile (development)

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS development
WORKDIR /app
ENV NODE_ENV=development
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app
USER nodejs
EXPOSE 3000 5173 9229
CMD ["npm", "run", "dev"]
```

### compose.override.yaml

```yaml
services:
  web:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - CHOKIDAR_USEPOLLING=true
    ports:
      - "3000:3000"
      - "5173:5173"
      - "9229:9229"
    stdin_open: true
    tty: true

  db:
    ports:
      - "5432:5432"
```

## Redis

```yaml
services:
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
```

## Elasticsearch

```yaml
services:
  elasticsearch:
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - es-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
      - "9300:9300"
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5

volumes:
  es-data:
```

## With Nginx Reverse Proxy

### nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }

    upstream api {
        server api:8000;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }

        location /api {
            proxy_pass http://api;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

### compose.yaml

```yaml
services:
  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
    depends_on:
      - frontend
      - api
```
