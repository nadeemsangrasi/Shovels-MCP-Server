---
name: scaffolding-fastapi
description: Scaffold production-ready FastAPI applications with proper project structure, routing, Pydantic models, database integration (SQLAlchemy/SQLModel), dependency injection, middleware, and authentication. Use when creating new FastAPI projects, setting up REST APIs, or building backend services with Python.
version: 1.0.0
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
author: Claude Code
tags: [fastapi, python, backend, api, rest, scaffolding, pydantic, sqlalchemy, async, database]
---

# FastAPI Scaffolding

Scaffold production-ready FastAPI applications with best practices for project structure, routing, validation, database integration, and authentication. Build high-performance async APIs with automatic documentation.

## Overview

FastAPI is a modern, fast Python web framework for building APIs. This skill helps you scaffold well-structured FastAPI projects with proper separation of concerns, dependency injection, async/await support, and production-ready patterns.

## When to Use This Skill

**Activate when:**
- Creating new FastAPI projects
- Setting up REST API structure
- Implementing CRUD endpoints
- Integrating databases (SQLAlchemy/SQLModel)
- Adding authentication/authorization
- Structuring async endpoints
- Setting up dependency injection

**Trigger keywords:** "fastapi", "scaffold fastapi", "rest api", "fastapi project", "api endpoints", "fastapi database", "pydantic models"

**NOT for:**
- Non-Python backends
- Simple scripts
- Django/Flask projects

## Prerequisites

**Required:**
- Python 3.8+
- pip or poetry
- Virtual environment knowledge

**Recommended:**
- Basic async/await understanding
- SQL database knowledge
- REST API concepts

## Instructions

### Phase 1: Project Setup

#### Step 1: Create Project Structure

**Quick:**
```bash
mkdir -p my-api/{app/{api,core,db,models,schemas},tests}
cd my-api
```

**Structure:**
```
my-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/          # API routes
│   ├── core/         # Config, security
│   ├── db/           # Database
│   ├── models/       # DB models
│   └── schemas/      # Pydantic schemas
├── tests/
├── requirements.txt
└── .env
```

**See:** `references/project-structure.md`

#### Step 2: Install FastAPI

**Quick:**
```bash
pip install "fastapi[standard]" uvicorn sqlalchemy pydantic-settings
```

**Or with poetry:**
```bash
poetry add fastapi uvicorn sqlalchemy pydantic-settings
```

**See:** `references/installation.md`

#### Step 3: Create Main Application

**Create `app/main.py`:**
```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

**See:** `references/examples.md#basic-app`

### Phase 2: Configuration

#### Step 4: Setup Configuration

**Create `app/core/config.py`:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "My API"
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
```

**See:** `references/configuration.md`

#### Step 5: Create Environment File

**`.env`:**
```env
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECRET_KEY=your-secret-key-min-32-chars
```

**See:** `references/configuration.md#env`

### Phase 3: Database Setup

#### Step 6: Configure Database

**Create `app/db/base.py`:**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

**See:** `references/database-setup.md`

#### Step 7: Create Database Dependency

**Create `app/db/session.py`:**
```python
from typing import Generator
from app.db.base import SessionLocal

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**See:** `references/examples.md#db-dependency`

### Phase 4: Models and Schemas

#### Step 8: Create Database Models

**Create `app/models/user.py`:**
```python
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
```

**See:** `references/models-guide.md`

#### Step 9: Create Pydantic Schemas

**Create `app/schemas/user.py`:**
```python
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
```

**See:** `references/schemas-guide.md`

### Phase 5: API Endpoints

#### Step 10: Create Router

**Create `app/api/users.py`:**
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import user as schemas

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[schemas.User])
async def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

**See:** `references/routing-guide.md`

#### Step 11: Register Router

**Update `app/main.py`:**
```python
from app.api import users

app.include_router(users.router)
```

**See:** `references/examples.md#routers`

### Phase 6: Dependency Injection

#### Step 12: Create Dependencies

**Common pattern:**
```python
from fastapi import Depends, HTTPException
from typing import Annotated

async def get_current_user(token: str):
    # Verify token
    return user

UserDep = Annotated[User, Depends(get_current_user)]

@router.get("/me")
async def read_me(user: UserDep):
    return user
```

**See:** `references/dependencies.md`

### Phase 7: Middleware

#### Step 13: Add Middleware

**CORS middleware:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**See:** `references/middleware-guide.md`

### Phase 8: Run and Test

#### Step 14: Run Application

**Quick:**
```bash
uvicorn app.main:app --reload
```

**Access docs:** `http://localhost:8000/docs`

**See:** `references/running-guide.md`

## Common Patterns

### Pattern 1: CRUD Operations
**Quick:** Model + Schema + Router with get/post/put/delete

**See:** `references/examples.md#crud`

### Pattern 2: Authentication
**Quick:** JWT tokens + password hashing + protected routes

**See:** `references/authentication.md`

### Pattern 3: Database Relationships
**Quick:** SQLAlchemy relationships + Pydantic nested schemas

**See:** `references/database-setup.md#relationships`

### Pattern 4: Background Tasks
**Quick:** Use BackgroundTasks for async operations

**See:** `references/examples.md#background-tasks`

### Pattern 5: File Uploads
**Quick:** UploadFile + save to disk/cloud

**See:** `references/examples.md#file-uploads`

## Project Structure Reference

```
my-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── api/
│   │   ├── __init__.py
│   │   ├── users.py         # User routes
│   │   └── items.py         # Item routes
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Settings
│   │   └── security.py      # Auth logic
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py          # SQLAlchemy base
│   │   └── session.py       # DB session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── item.py          # Item model
│   └── schemas/
│       ├── __init__.py
│       ├── user.py          # User schemas
│       └── item.py          # Item schemas
├── tests/
│   ├── test_api.py
│   └── test_models.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

**See:** `references/project-structure.md`

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Import errors | Wrong Python path | Set PYTHONPATH or use `python -m` |
| Database connection failed | Wrong DATABASE_URL | Check .env configuration |
| Pydantic validation errors | Schema mismatch | Verify model/schema alignment |
| 422 Unprocessable Entity | Invalid request data | Check Pydantic schema |
| Dependency injection fails | Wrong type hints | Use Annotated or Depends correctly |

**See:** `references/troubleshooting.md`

## FastAPI Features

**Auto Docs:** `/docs` (Swagger), `/redoc`, `/openapi.json`
**Validation:** Pydantic models, type hints
**Performance:** Async/await, background tasks, WebSocket
**Security:** OAuth2/JWT, API keys, CORS

**Integration:** Next.js (CORS), PostgreSQL (SQLAlchemy), Auth (JWT/bcrypt)

**See:** `references/features-reference.md`, `references/integrations.md`

## Best Practices

1. **Dependency injection** - Reusable, testable | 2. **Pydantic validation** - Type-safe I/O | 3. **Async I/O** - Better performance | 4. **Separate schemas/models** - Clear separation | 5. **Environment config** - Use .env | 6. **Router organization** - Group endpoints | 7. **Error handling** - HTTPException | 8. **Documentation** - Describe endpoints

## Validation Checklist

**Project Setup:** [ ] venv, dependencies, .env, .gitignore
**Structure:** [ ] Folders, __init__.py, imports
**Database:** [ ] Models, schemas, DI, migrations
**API:** [ ] Routers, docs, response models, errors
**Testing:** [ ] /docs accessible, endpoints work, validation, DB ops

## Quick Commands

**Setup:** `python -m venv venv`, activate venv, `pip install -r requirements.txt`
**Run:** `uvicorn app.main:app --reload`
**Custom:** `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## References

**Local Documentation:**
- Project structure: `references/project-structure.md`
- Installation: `references/installation.md`
- Configuration: `references/configuration.md`
- Database setup: `references/database-setup.md`
- Models guide: `references/models-guide.md`
- Schemas guide: `references/schemas-guide.md`
- Routing guide: `references/routing-guide.md`
- Dependencies: `references/dependencies.md`
- Middleware guide: `references/middleware-guide.md`
- Authentication: `references/authentication.md`
- Examples: `references/examples.md`
- Troubleshooting: `references/troubleshooting.md`

**External Resources:**
- [FastAPI Official Documentation](https://fastapi.tiangolo.com)
- [FastAPI GitHub](https://github.com/fastapi/fastapi)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)

## Tips for Success

1. **Start with structure** - Organize early | 2. **Use type hints** - FastAPI core feature | 3. **Test early** - Use /docs | 4. **Focused routers** - One resource per router | 5. **Dependency injection** - Reduces boilerplate | 6. **Document ongoing** - Add descriptions | 7. **Async wisely** - I/O only | 8. **Version API** - `/api/v1/`

## Version History

**v1.0.0 (2026-01-01)** - Initial release with project scaffolding, SQLAlchemy integration, Pydantic validation, routing, DI, middleware, auth guidance, Context7 MCP

## Sources

- [FastAPI Official Documentation](https://fastapi.tiangolo.com)
- [FastAPI on Context7](https://context7.com/fastapi/fastapi)
- FastAPI GitHub Repository
