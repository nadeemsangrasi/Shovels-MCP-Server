#!/bin/bash
# FastAPI Project Initialization Script

PROJECT_NAME="${1:-my-fastapi-project}"

echo "Creating FastAPI project: $PROJECT_NAME"

# Create directory structure
mkdir -p "$PROJECT_NAME"/{app/{api,core,db,models,schemas},tests,scripts,alembic/versions}

# Create __init__.py files
touch "$PROJECT_NAME"/app/__init__.py
touch "$PROJECT_NAME"/app/api/__init__.py
touch "$PROJECT_NAME"/app/core/__init__.py
touch "$PROJECT_NAME"/app/db/__init__.py
touch "$PROJECT_NAME"/app/models/__init__.py
touch "$PROJECT_NAME"/app/schemas/__init__.py
touch "$PROJECT_NAME"/tests/__init__.py

echo "✓ Project structure created"
echo ""
echo "Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. python -m venv venv && source venv/bin/activate"
echo "3. Copy .env.example to .env and update settings"
echo "4. pip install -r requirements.txt"
echo "5. Start coding!"
