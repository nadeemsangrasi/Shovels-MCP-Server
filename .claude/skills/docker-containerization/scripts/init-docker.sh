#!/bin/bash

# Docker Containerization Project Initializer
# Usage: ./init-docker.sh [node|python|static] [project-name]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
TYPE=${1:-node}
PROJECT_NAME=${2:-myapp}

echo -e "${GREEN}Initializing Docker project: ${PROJECT_NAME}${NC}"
echo -e "${GREEN}Type: ${TYPE}${NC}"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="${SCRIPT_DIR}/../assets/templates"

# Create project directory
mkdir -p "${PROJECT_NAME}"
cd "${PROJECT_NAME}"

# Copy .dockerignore
cp "${TEMPLATES_DIR}/.dockerignore" ./

# Copy .env.example
cp "${TEMPLATES_DIR}/.env.example" ./

# Copy Docker Compose
cp "${TEMPLATES_DIR}/compose.yaml" ./

# Copy Dockerfile based on type
case "${TYPE}" in
    node)
        echo -e "${GREEN}Setting up Node.js project...${NC}"
        cp "${TEMPLATES_DIR}/Dockerfile-nodejs" ./Dockerfile

        if [ -f package.json ]; then
            echo -e "${GREEN}package.json found${NC}"
        else
            echo -e "${YELLOW}package.json not found. Creating minimal one...${NC}"
            cat > package.json << 'EOF'
{
  "name": "myapp",
  "version": "1.0.0",
  "scripts": {
    "start": "node dist/server.js",
    "build": "tsc",
    "dev": "ts-node src/index.ts"
  }
}
EOF
        fi
        ;;

    python)
        echo -e "${GREEN}Setting up Python project...${NC}"
        cp "${TEMPLATES_DIR}/Dockerfile-python" ./Dockerfile

        if [ -f requirements.txt ]; then
            echo -e "${GREEN}requirements.txt found${NC}"
        else
            echo -e "${YELLOW}requirements.txt not found. Creating minimal one...${NC}"
            cat > requirements.txt << 'EOF'
fastapi==0.109.0
uvicorn==0.27.0
gunicorn==21.2.0
EOF
        fi
        ;;

    static)
        echo -e "${GREEN}Setting up static site project...${NC}"
        cp "${TEMPLATES_DIR}/Dockerfile-static" ./Dockerfile

        # Create nginx config
        cat > nginx.conf << 'EOF'
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
}
EOF
        ;;

    *)
        echo -e "${RED}Unknown project type: ${TYPE}${NC}"
        echo -e "${YELLOW}Valid types: node, python, static${NC}"
        exit 1
        ;;
esac

# Create docker-compose override for development
cat > compose.override.yaml << EOF
services:
  web:
    build:
      target: production
    volumes:
      - ./:/app
    environment:
      - NODE_ENV=development
    stdin_open: true
    tty: true
EOF

echo -e "${GREEN}Done!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Update .env with your configuration"
echo "2. Update Dockerfile with your application specifics"
echo "3. Run: docker compose up -d"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "  docker compose up -d     # Start services"
echo "  docker compose logs -f   # View logs"
echo "  docker compose down      # Stop services"
