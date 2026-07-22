# FastAPI Installation Guide

## Prerequisites

### Python Version

FastAPI requires Python 3.8 or higher. Check your version:

```bash
python --version
# or
python3 --version
```

### Package Manager

Choose one:
- **pip** - Standard Python package installer (included with Python)
- **poetry** - Modern dependency management and packaging
- **pip-tools** - Pip with requirements compilation

## Installation Methods

### Method 1: pip with Standard Installation

**Basic installation:**
```bash
pip install fastapi
```

**With all optional dependencies:**
```bash
pip install "fastapi[standard]"
```

This includes:
- `uvicorn[standard]` - ASGI server with auto-reload
- `pydantic-settings` - Settings management
- `pydantic-extra-types` - Extra Pydantic types
- `fastapi-cli` - FastAPI CLI tool
- `python-multipart` - Form data support
- `jinja2` - HTML templates
- `python-email-validator` - Email validation

**Production-ready installation:**
```bash
pip install fastapi uvicorn[standard] sqlalchemy pydantic-settings python-multipart
```

### Method 2: Poetry (Recommended for Projects)

**Install Poetry:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Create new project:**
```bash
poetry new my-fastapi-project
cd my-fastapi-project
```

**Add FastAPI dependencies:**
```bash
poetry add fastapi uvicorn[standard] sqlalchemy pydantic-settings
```

**Add development dependencies:**
```bash
poetry add --group dev pytest httpx black mypy
```

**Install dependencies:**
```bash
poetry install
```

**Activate virtual environment:**
```bash
poetry shell
```

### Method 3: pip with Virtual Environment

**Create virtual environment:**
```bash
# Unix/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**requirements.txt:**
```
fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.36
pydantic-settings==2.6.0
python-multipart==0.0.12
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
```

## Core Dependencies

### Required Packages

**fastapi**
- Core FastAPI framework
- Automatic API documentation
- Data validation via Pydantic

```bash
pip install fastapi
```

**uvicorn**
- ASGI server to run FastAPI
- Development server with hot reload
- Production-ready

```bash
pip install "uvicorn[standard]"
```

### Common Optional Dependencies

**Database:**
```bash
# SQLAlchemy ORM
pip install sqlalchemy

# Async SQLAlchemy
pip install sqlalchemy[asyncio]

# PostgreSQL driver
pip install psycopg2-binary  # or asyncpg for async

# MySQL driver
pip install pymysql

# SQLite (included in Python standard library)
```

**Authentication:**
```bash
# JWT tokens
pip install python-jose[cryptography]

# Password hashing
pip install passlib[bcrypt]

# OAuth2 (optional, for third-party auth)
pip install python-oauth2
```

**Configuration:**
```bash
# Environment variable management
pip install python-dotenv

# Settings from .env files
pip install pydantic-settings
```

**Forms and File Uploads:**
```bash
# Form data and file uploads
pip install python-multipart
```

**Email Validation:**
```bash
# Email field validation
pip install email-validator
```

**Development Tools:**
```bash
# Testing
pip install pytest httpx

# Code formatting
pip install black

# Type checking
pip install mypy

# Linting
pip install ruff

# Auto-reload for development
pip install watchfiles
```

## Database Drivers

### PostgreSQL

**Synchronous:**
```bash
pip install psycopg2-binary
```

**Async:**
```bash
pip install asyncpg
```

**Connection string:**
```
postgresql://user:password@localhost:5432/dbname
# Async
postgresql+asyncpg://user:password@localhost:5432/dbname
```

### MySQL/MariaDB

**Synchronous:**
```bash
pip install pymysql
```

**Async:**
```bash
pip install aiomysql
```

**Connection string:**
```
mysql+pymysql://user:password@localhost:3306/dbname
# Async
mysql+aiomysql://user:password@localhost:3306/dbname
```

### SQLite

**Built-in (no installation needed):**
```python
DATABASE_URL = "sqlite:///./app.db"
```

**Async:**
```bash
pip install aiosqlite
```

```python
DATABASE_URL = "sqlite+aiosqlite:///./app.db"
```

## requirements.txt Templates

### Minimal (Development)

```
fastapi==0.115.0
uvicorn[standard]==0.32.0
```

### Standard (Production-Ready)

```
# Core
fastapi==0.115.0
uvicorn[standard]==0.32.0

# Database
sqlalchemy==2.0.36
psycopg2-binary==2.9.9

# Configuration
pydantic-settings==2.6.0
python-dotenv==1.0.0

# Forms
python-multipart==0.0.12
```

### Complete (With Auth)

```
# Core
fastapi==0.115.0
uvicorn[standard]==0.32.0

# Database
sqlalchemy==2.0.36
psycopg2-binary==2.9.9
alembic==1.13.1

# Configuration
pydantic-settings==2.6.0
python-dotenv==1.0.0

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Validation
email-validator==2.1.0
python-multipart==0.0.12

# Development
pytest==8.0.0
httpx==0.26.0
black==24.1.1
mypy==1.8.0
```

## pyproject.toml Template (Poetry)

```toml
[tool.poetry]
name = "my-fastapi-project"
version = "1.0.0"
description = "A production-ready FastAPI application"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.115.0"
uvicorn = {extras = ["standard"], version = "^0.32.0"}
sqlalchemy = "^2.0.36"
pydantic-settings = "^2.6.0"
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
psycopg2-binary = "^2.9.9"
alembic = "^1.13.1"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
httpx = "^0.26.0"
black = "^24.1.1"
mypy = "^1.8.0"
ruff = "^0.1.15"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 100
target-version = ['py311']

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.ruff]
line-length = 100
select = ["E", "F", "I"]
```

## Verification

### Verify Installation

```bash
# Check FastAPI version
python -c "import fastapi; print(fastapi.__version__)"

# Check uvicorn
python -c "import uvicorn; print(uvicorn.__version__)"

# List all installed packages
pip list

# Or with poetry
poetry show
```

### Test Installation

**Create test file `test.py`:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FastAPI is working!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Run:**
```bash
python test.py
```

**Visit:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

## Common Installation Issues

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
# Ensure you're in the correct virtual environment
which python  # Unix/macOS
where python  # Windows

# Install FastAPI
pip install fastapi
```

### Issue: "uvicorn: command not found"

**Solution:**
```bash
# Install uvicorn
pip install "uvicorn[standard]"

# Or run via Python module
python -m uvicorn app.main:app --reload
```

### Issue: PostgreSQL driver errors

**Solution:**
```bash
# For macOS (if psycopg2 fails)
brew install postgresql
pip install psycopg2-binary

# For Ubuntu/Debian
sudo apt-get install libpq-dev
pip install psycopg2-binary

# Or use pure Python driver
pip install psycopg2-binary
```

### Issue: "cryptography" build errors

**Solution:**
```bash
# Install build dependencies
# macOS
brew install openssl rust

# Ubuntu/Debian
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev

# Then install
pip install cryptography
```

## Docker Installation

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application
COPY ./app ./app

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

**Run:**
```bash
docker-compose up --build
```

## Platform-Specific Notes

### Windows

- Use `py` instead of `python` if you have multiple Python versions
- Use `venv\Scripts\activate` to activate virtual environment
- Consider using WSL2 for better compatibility

### macOS

- Use Homebrew to install system dependencies: `brew install postgresql`
- May need Xcode command line tools: `xcode-select --install`

### Linux

- Install build dependencies: `sudo apt-get install build-essential python3-dev`
- Use `python3` and `pip3` explicitly if Python 2 is also installed

## Next Steps

After installation:
1. Create project structure (see project-structure.md)
2. Configure database (see database-setup.md)
3. Set up authentication (see authentication.md)
4. Start building endpoints (see examples.md)
