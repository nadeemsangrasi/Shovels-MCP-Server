# Multi-Stage Builds

Multi-stage builds allow you to use multiple FROM instructions in a single Dockerfile, separating build and runtime environments for smaller, more secure production images.

## Why Multi-Stage Builds

- **Smaller images** - Only production artifacts in final image
- **Better security** - Build tools not included in production
- **Cleaner separation** - Build vs runtime concerns
- **Faster deployments** - Smaller images transfer quicker

## Pattern 1: Node.js with Build Step

```dockerfile
# syntax=docker/dockerfile:1

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
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Pattern 2: Node.js Full Multi-Stage

```dockerfile
ARG NODE_VERSION=20-alpine

# Base stage
FROM node:${NODE_VERSION} AS base
WORKDIR /app

# Dependencies stage
FROM base AS deps
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev
RUN npm cache clean --force

# Build dependencies
FROM base AS build-deps
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .

# Build stage
FROM build-deps AS build
RUN npm run build

# Production stage
FROM base AS production
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
USER nodejs
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

## Pattern 3: Python with Gunicorn

```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim AS production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
RUN adduser --system --group appuser
USER appuser
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

## Pattern 4: Go/Rust (Compiled Languages)

```dockerfile
# Build stage
FROM golang:1.21-alpine AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Production stage
FROM scratch
COPY --from=build /src/main /main
EXPOSE 8080
CMD ["/main"]
```

## Pattern 5: React/Vue Frontend

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
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Pattern 6: PHP with Laravel

```dockerfile
# PHP build stage
FROM composer:2 AS composer
COPY composer.json composer.lock ./
RUN composer install --no-dev --optimize-autoloader

# PHP runtime stage
FROM php:8.2-fpm-alpine
WORKDIR /var/www
COPY --from=composer /app/vendor /var/www/vendor
COPY . .
RUN chmod -R 755 storage bootstrap/cache
EXPOSE 9000
CMD ["php-fpm"]
```

## Using Build Arguments (ARG)

```dockerfile
ARG NODE_VERSION=20-alpine
FROM node:${NODE_VERSION} AS base

# Use ARG in production
FROM base AS production
ARG BUILD_VERSION
ENV APP_VERSION=${BUILD_VERSION}
```

```bash
docker build --build-arg BUILD_VERSION=1.0.0 -t myapp .
```

## Copying Between Stages

```dockerfile
# By name (AS alias)
COPY --from=build /app/dist /usr/share/nginx/html

# By index (0-based)
COPY --from=0 /app/dist /usr/share/nginx/html

# External image
COPY --from=nginx:alpine /etc/nginx/nginx.conf /etc/nginx/
```

## Best Practices

1. **Use specific base image tags** - Avoid `latest`
2. **Order instructions for caching** - Files that change less frequently first
3. **Use `--mount=type=cache`** - For package manager caches
4. **Minimize layers** - Combine related RUN commands
5. **Remove unnecessary files** - Clean up in the same layer
6. **Use appropriate base images** - Alpine for smaller size
