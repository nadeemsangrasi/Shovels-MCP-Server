# FastAPI Configuration Guide

## Configuration Management with Pydantic Settings

FastAPI uses Pydantic Settings for type-safe configuration management that automatically loads from environment variables and `.env` files.

### Basic Configuration Setup

**app/core/config.py:**
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "My FastAPI Project"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

settings = Settings()
```

### .env File

**.env (Development):**
```env
# Application
PROJECT_NAME="My FastAPI Project"
VERSION="1.0.0"
API_V1_STR="/api/v1"

# Security
SECRET_KEY="your-secret-key-here-min-32-characters-long"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"

# CORS
ALLOWED_ORIGINS='["http://localhost:3000","http://localhost:8080"]'

# Email (Optional)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
EMAIL_FROM="noreply@example.com"

# Redis (Optional)
REDIS_URL="redis://localhost:6379/0"

# Environment
ENVIRONMENT="development"
DEBUG=true
```

**.env.example (Template for version control):**
```env
# Application
PROJECT_NAME="My FastAPI Project"
VERSION="1.0.0"
API_V1_STR="/api/v1"

# Security (REQUIRED)
SECRET_KEY="change-this-to-a-secure-random-string"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (REQUIRED)
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"

# CORS
ALLOWED_ORIGINS='["http://localhost:3000"]'

# Email (Optional)
SMTP_HOST=""
SMTP_PORT=587
SMTP_USER=""
SMTP_PASSWORD=""
EMAIL_FROM=""

# Environment
ENVIRONMENT="development"
DEBUG=true
```

## Advanced Configuration

### Environment-Specific Settings

**app/core/config.py:**
```python
from typing import List, Literal
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = False

    # Application
    PROJECT_NAME: str = "My FastAPI Project"
    PROJECT_DESCRIPTION: str = "A production-ready FastAPI application"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str
    DB_ECHO: bool = False  # SQLAlchemy echo SQL queries
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [".jpg", ".jpeg", ".png", ".pdf"]

    # Email
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = ""

    # Redis (Optional)
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 300  # 5 minutes

    # AWS S3 (Optional)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = ""

    # Monitoring
    SENTRY_DSN: str = ""

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignore extra env variables
    )

settings = Settings()
```

### Multiple Environment Files

**Development (.env.development):**
```env
ENVIRONMENT="development"
DEBUG=true
DATABASE_URL="sqlite:///./dev.db"
ALLOWED_ORIGINS='["http://localhost:3000"]'
```

**Production (.env.production):**
```env
ENVIRONMENT="production"
DEBUG=false
DATABASE_URL="postgresql://user:password@prod-db:5432/dbname"
ALLOWED_ORIGINS='["https://myapp.com","https://www.myapp.com"]'
SENTRY_DSN="https://your-sentry-dsn"
```

**Load specific environment:**
```python
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('ENVIRONMENT', 'development')}",
        case_sensitive=True
    )
```

## Database Configuration

### PostgreSQL

```env
# Standard connection
DATABASE_URL="postgresql://username:password@localhost:5432/database_name"

# With options
DATABASE_URL="postgresql://user:pass@localhost:5432/db?sslmode=require&connect_timeout=10"

# Connection pool settings
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

### SQLAlchemy Engine Configuration

```python
from sqlalchemy import create_engine
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,  # Verify connections before using
    echo=settings.DB_ECHO  # Log SQL queries
)
```

### Async Database

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

async_engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.DB_ECHO,
    future=True
)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

## Security Configuration

### Secret Key Generation

```python
# Generate secure secret key
import secrets

secret_key = secrets.token_urlsafe(32)
print(f"SECRET_KEY={secret_key}")
```

### Password Hashing Configuration

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Higher is more secure but slower
)
```

### JWT Configuration

```env
# .env
SECRET_KEY="your-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

```python
# app/core/security.py
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
```

## CORS Configuration

### Basic CORS

```python
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Strict CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,  # Cache preflight requests
)
```

## Logging Configuration

### Basic Logging

```python
# app/core/logging.py
import logging
from app.core.config import settings

def setup_logging():
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Reduce noise from libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
```

### Structured Logging

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logging.root.addHandler(handler)
    logging.root.setLevel(logging.INFO)
```

## Email Configuration

```env
# Gmail
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
EMAIL_FROM="noreply@yourapp.com"

# SendGrid
SMTP_HOST="smtp.sendgrid.net"
SMTP_PORT=587
SMTP_USER="apikey"
SMTP_PASSWORD="your-sendgrid-api-key"
EMAIL_FROM="noreply@yourapp.com"

# AWS SES
SMTP_HOST="email-smtp.us-east-1.amazonaws.com"
SMTP_PORT=587
SMTP_USER="your-smtp-username"
SMTP_PASSWORD="your-smtp-password"
EMAIL_FROM="noreply@yourapp.com"
```

## Testing Configuration

### Test Settings

```python
# app/core/config.py
class TestSettings(Settings):
    ENVIRONMENT: str = "testing"
    DATABASE_URL: str = "sqlite:///./test.db"
    DEBUG: bool = True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5

    model_config = SettingsConfigDict(
        env_file=".env.test",
        case_sensitive=True
    )

# tests/conftest.py
from app.core.config import TestSettings

test_settings = TestSettings()
```

## Configuration Best Practices

### 1. Never Commit Secrets

**.gitignore:**
```
.env
.env.local
.env.*.local
*.key
*.pem
```

### 2. Use Strong Types

```python
from pydantic import PostgresDsn, HttpUrl, EmailStr

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    WEBSITE_URL: HttpUrl
    ADMIN_EMAIL: EmailStr
```

### 3. Validate Configuration on Startup

```python
# app/main.py
from app.core.config import settings

@app.on_event("startup")
async def validate_config():
    assert settings.SECRET_KEY, "SECRET_KEY must be set"
    assert len(settings.SECRET_KEY) >= 32, "SECRET_KEY must be at least 32 characters"
    assert settings.DATABASE_URL, "DATABASE_URL must be set"
```

### 4. Environment-Specific Defaults

```python
class Settings(BaseSettings):
    # Development defaults
    DEBUG: bool = True
    DB_ECHO: bool = True

    # Override in production
    @field_validator("DEBUG")
    @classmethod
    def set_production_defaults(cls, v, info):
        if info.data.get("ENVIRONMENT") == "production":
            return False
        return v
```

### 5. Document Required Variables

Create a `CONFIGURATION.md` file:

```markdown
# Required Environment Variables

## Application
- `PROJECT_NAME`: Application name (default: "My FastAPI Project")
- `VERSION`: API version (default: "1.0.0")

## Security (REQUIRED)
- `SECRET_KEY`: Secret key for JWT tokens (min 32 characters)
- `ALGORITHM`: JWT algorithm (default: "HS256")

## Database (REQUIRED)
- `DATABASE_URL`: PostgreSQL connection string

## Optional
- `ALLOWED_ORIGINS`: Comma-separated list of CORS origins
- `SMTP_*`: Email configuration for notifications
```

## Docker Configuration

### docker-compose.yml with environment

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env.production
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
    depends_on:
      - db

  db:
    image: postgres:15
    env_file:
      - .env.production
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
```

## Troubleshooting

### Issue: "Field required" error on startup

**Cause:** Required environment variable not set

**Solution:**
```bash
# Check which variable is missing
python -c "from app.core.config import settings; print(settings)"

# Set in .env file or export
export SECRET_KEY="your-secret-key"
```

### Issue: Type validation error

**Cause:** Environment variable value doesn't match expected type

**Solution:**
```python
# Debug validation
from pydantic import ValidationError
try:
    settings = Settings()
except ValidationError as e:
    print(e.json())
```

### Issue: .env file not loaded

**Cause:** Wrong file path or encoding

**Solution:**
```python
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8"
    )
```
