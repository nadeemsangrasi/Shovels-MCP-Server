# FastAPI Project Structure Guide

## Standard Project Layout

```
my-fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Application entry point
│   ├── api/                     # API route handlers
│   │   ├── __init__.py
│   │   ├── deps.py              # Shared dependencies
│   │   ├── users.py             # User endpoints
│   │   ├── posts.py             # Post endpoints
│   │   └── auth.py              # Authentication endpoints
│   ├── core/                    # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py            # Settings and configuration
│   │   ├── security.py          # Security utilities
│   │   └── logging.py           # Logging configuration
│   ├── db/                      # Database
│   │   ├── __init__.py
│   │   ├── base.py              # SQLAlchemy base and engine
│   │   └── session.py           # Database session management
│   ├── models/                  # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   └── post.py              # Post model
│   ├── schemas/                 # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py              # User schemas
│   │   ├── post.py              # Post schemas
│   │   └── token.py             # Token schemas
│   ├── crud/                    # CRUD operations (optional)
│   │   ├── __init__.py
│   │   ├── base.py              # Base CRUD class
│   │   ├── user.py              # User CRUD
│   │   └── post.py              # Post CRUD
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── alembic/                     # Database migrations
│   ├── versions/
│   └── env.py
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_api/
│   │   ├── test_users.py
│   │   └── test_posts.py
│   └── test_crud/
│       └── test_user_crud.py
├── scripts/                     # Utility scripts
│   ├── init_db.py               # Database initialization
│   └── seed_data.py             # Seed data
├── .env                         # Environment variables
├── .env.example                 # Example environment file
├── .gitignore
├── alembic.ini                  # Alembic configuration
├── pyproject.toml               # Poetry configuration
├── requirements.txt             # Pip requirements
└── README.md
```

## File Purposes

### Root Directory

**`.env`**
- Environment-specific configuration
- Database URLs, API keys, secrets
- Never commit to version control

**`.env.example`**
- Template for `.env` file
- Shows required environment variables
- Safe to commit to version control

**`requirements.txt`**
- Python dependencies for pip
- Generated from `pyproject.toml` or manually maintained

**`pyproject.toml`**
- Poetry configuration
- Project metadata and dependencies
- Development dependencies

**`alembic.ini`**
- Alembic migration tool configuration
- Database connection settings

### app/main.py

Application entry point and FastAPI instance creation.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import users, posts, auth

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(posts.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### app/core/config.py

Application configuration using pydantic-settings.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # API
    PROJECT_NAME: str = "My FastAPI Project"
    PROJECT_DESCRIPTION: str = "A production-ready FastAPI application"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    # Email (optional)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

settings = Settings()
```

### app/db/base.py

SQLAlchemy engine and base class.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False  # Set to True for SQL logging
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Import all models here for Alembic
from app.models.user import User
from app.models.post import Post
```

### app/db/session.py

Database session dependency.

```python
from typing import Generator
from app.db.base import SessionLocal

def get_db() -> Generator:
    """
    Database session dependency.

    Yields:
        SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### app/api/deps.py

Shared API dependencies.

```python
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current superuser."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges"
        )
    return current_user
```

## Directory Organization Strategies

### Strategy 1: Feature-Based Structure

Organize by feature/domain instead of technical layer:

```
app/
├── main.py
├── core/
├── users/
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   └── crud.py
├── posts/
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   └── crud.py
└── auth/
    ├── schemas.py
    ├── routes.py
    └── security.py
```

**Pros:**
- Clear feature boundaries
- Easy to find related code
- Good for microservices migration

**Cons:**
- More complex imports
- Potential circular dependencies

### Strategy 2: Layered Architecture (Recommended)

Organize by technical layer (shown in main structure above):

**Pros:**
- Clear separation of concerns
- Easier to understand
- Standard FastAPI pattern

**Cons:**
- Related code spread across directories
- More files to navigate

### Strategy 3: Hybrid Approach

Combine both strategies:

```
app/
├── main.py
├── core/
│   ├── config.py
│   └── security.py
├── common/
│   ├── db/
│   └── schemas/
└── features/
    ├── users/
    │   ├── models.py
    │   ├── schemas.py
    │   ├── routes.py
    │   └── crud.py
    └── posts/
        ├── models.py
        ├── schemas.py
        ├── routes.py
        └── crud.py
```

## Scaling Considerations

### Small Projects (< 5 endpoints)

```
app/
├── main.py
├── models.py
├── schemas.py
└── config.py
```

### Medium Projects (5-20 endpoints)

Use the standard structure shown above.

### Large Projects (20+ endpoints)

Consider:
- Feature-based modules
- Separate packages for domains
- API versioning structure:

```
app/
├── api/
│   ├── v1/
│   │   ├── users.py
│   │   └── posts.py
│   └── v2/
│       ├── users.py
│       └── posts.py
```

## Best Practices

1. **Keep `main.py` minimal** - Only app creation and router registration
2. **Use `__init__.py` files** - For cleaner imports
3. **Separate concerns** - Models, schemas, and routes in different files
4. **Use dependencies** - Leverage FastAPI's dependency injection
5. **Configuration management** - Environment-based settings
6. **Type hints everywhere** - FastAPI relies on them
7. **Consistent naming** - Use plural for collections (users.py, not user.py for routes)
8. **Import organization** - Standard library, third-party, local

## Common Patterns

### Router Registration Pattern

```python
# app/api/__init__.py
from fastapi import APIRouter
from app.api import users, posts, auth

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(posts.router, tags=["posts"])

# app/main.py
from app.api import api_router
app.include_router(api_router, prefix="/api/v1")
```

### Database Model Import Pattern

```python
# app/db/base.py
from app.db.base_class import Base

# Import all models here so Alembic can detect them
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
```

### Shared Dependency Pattern

```python
# app/api/deps.py
from typing import Annotated
from fastapi import Depends

# Create type aliases for common dependencies
DbSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_active_user)]

# Usage in routes
@router.get("/me")
async def read_me(current_user: CurrentUser):
    return current_user
```

## Migration Path

### From Monolithic to Modular

1. Start with simple structure
2. Extract common patterns into `crud/` and `utils/`
3. Split large route files by resource
4. Consider feature modules when > 10 related endpoints
5. Introduce API versioning when breaking changes needed
