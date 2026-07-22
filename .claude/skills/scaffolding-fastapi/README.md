# FastAPI Scaffolding Skill

A comprehensive Claude Code skill for scaffolding production-ready FastAPI applications with proper project structure, database integration, authentication, and best practices.

## Overview

This skill guides you through creating well-structured FastAPI projects with SQLAlchemy/SQLModel, Pydantic validation, dependency injection, middleware, and authentication patterns. Build high-performance async APIs with automatic documentation.

## Features

### ✅ Project Scaffolding
- Standard directory structure
- Configuration management with pydantic-settings
- Environment variable handling
- Virtual environment setup

### ✅ Database Integration
- SQLAlchemy ORM setup
- Database models and relationships
- Migration management with Alembic
- Connection pooling
- PostgreSQL, MySQL, SQLite support

### ✅ API Development
- Router organization
- CRUD operations
- Request/response validation with Pydantic
- Dependency injection patterns
- Error handling

### ✅ Authentication
- JWT token-based authentication
- Password hashing with bcrypt
- OAuth2 integration
- Role-based access control (RBAC)
- Protected routes

### ✅ Production Ready
- CORS middleware
- Background tasks
- File uploads
- WebSocket support
- Logging configuration
- Testing patterns

## Installation

### Prerequisites

- Python 3.8+
- pip or Poetry
- Virtual environment tool (venv, virtualenv, etc.)
- PostgreSQL/MySQL/SQLite (depending on your choice)

### Skill Installation

```bash
# Copy to project skills
cp -r scaffolding-fastapi /path/to/project/.claude/skills/

# Or copy to global skills
cp -r scaffolding-fastapi ~/.claude/skills/
```

## Usage

### Activation

The skill activates with trigger keywords:
- "fastapi"
- "scaffold fastapi"
- "rest api"
- "fastapi project"
- "api endpoints"
- "fastapi database"
- "pydantic models"

### Quick Start

**Create a new FastAPI project:**
```bash
# 1. Create project structure
mkdir -p my-api/{app/{api,core,db,models,schemas},tests}
cd my-api

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install "fastapi[standard]" uvicorn sqlalchemy pydantic-settings

# 4. Create main.py
cat > app/main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World"}
EOF

# 5. Run the application
uvicorn app.main:app --reload

# 6. Visit http://localhost:8000/docs for interactive API docs
```

### Example Prompts

**Project Setup:**
- "Create a FastAPI project with PostgreSQL"
- "Set up FastAPI with SQLAlchemy and Pydantic"
- "Initialize FastAPI project structure"

**Database:**
- "Add database models for users and posts"
- "Set up Alembic migrations"
- "Create SQLAlchemy relationships"

**Authentication:**
- "Implement JWT authentication"
- "Add OAuth2 login flow"
- "Create protected routes"

**API Development:**
- "Create CRUD endpoints for users"
- "Add file upload endpoint"
- "Implement pagination"

## Documentation Structure

```
scaffolding-fastapi/
├── SKILL.md (441 lines)              # Main workflow
├── README.md                          # This file
├── references/
│   ├── examples.md                    # Complete implementations
│   ├── project-structure.md           # Directory organization
│   ├── installation.md                # Setup guide
│   ├── configuration.md               # Settings management
│   ├── database-setup.md              # SQLAlchemy setup
│   ├── models-guide.md                # Database models
│   ├── schemas-guide.md               # Pydantic schemas
│   ├── routing-guide.md               # API routes
│   ├── dependencies.md                # Dependency injection
│   ├── middleware-guide.md            # Middleware setup
│   ├── authentication.md              # Auth patterns
│   └── troubleshooting.md             # Common issues
├── assets/
│   └── templates/
│       ├── .env.example               # Environment template
│       ├── alembic.ini                # Migration config
│       └── requirements.txt           # Dependencies
└── scripts/
    └── init-project.sh                # Quick setup script
```

## Key Concepts

### Project Structure

FastAPI applications follow a layered architecture:

- **app/main.py** - Application entry point
- **app/api/** - Route handlers (endpoints)
- **app/core/** - Configuration and security
- **app/db/** - Database connection and session
- **app/models/** - SQLAlchemy models
- **app/schemas/** - Pydantic schemas
- **app/crud/** - CRUD operations (optional)
- **tests/** - Test suite

### Configuration Management

Use pydantic-settings for type-safe configuration:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
```

### Database Models vs Schemas

**Models** (SQLAlchemy) - Database tables:
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
```

**Schemas** (Pydantic) - Request/response validation:
```python
class UserCreate(BaseModel):
    email: EmailStr
    password: str
```

### Dependency Injection

FastAPI's dependency system for reusable logic:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users/")
async def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

## Common Use Cases

### REST API with CRUD Operations
Create full CRUD endpoints for resources with database persistence

### Authentication System
JWT-based authentication with user registration and login

### Data Validation API
Use Pydantic for request/response validation and type safety

### File Upload Service
Handle file uploads with size limits and type validation

### Background Task Processing
Run tasks asynchronously without blocking requests

### Microservice Backend
Build scalable backend services with async support

## Integration with Other Skills

### With better-auth-nextjs
- FastAPI as backend API
- Next.js as frontend
- JWT tokens for authentication
- CORS configuration for cross-origin requests

### With nextjs-dev-tool
- Test API endpoints during development
- Verify CORS settings
- Debug request/response flow

### With modern-ui-ux-theming
- Design consistent API response formats
- Implement consistent error handling
- Design API documentation

See `references/integration-guides.md` for detailed workflows (when created).

## Best Practices

1. **Use dependency injection** - Reusable, testable code
2. **Pydantic for validation** - Type-safe request/response
3. **Async for I/O** - Better performance for database and network operations
4. **Separate schemas from models** - Clear separation of concerns
5. **Environment variables** - Never hardcode secrets
6. **Router organization** - Group related endpoints
7. **Error handling** - Use HTTPException with proper status codes
8. **Documentation** - Add docstrings and descriptions to endpoints

## FastAPI Features

### Automatic API Documentation
- **/docs** - Interactive Swagger UI
- **/redoc** - Alternative ReDoc documentation
- **/openapi.json** - OpenAPI schema

### Data Validation
- Automatic request validation with Pydantic
- Type hints for parameters
- Response model validation

### Performance
- Async/await support
- High performance (comparable to NodeJS and Go)
- Automatic JSON serialization

### Developer Experience
- Auto-completion everywhere
- Minimal code duplication
- Easy testing

## Requirements

**Minimum:**
- Python 3.8+
- FastAPI 0.100.0+
- Uvicorn 0.20.0+
- SQLAlchemy 2.0.0+
- Pydantic 2.0.0+

**Recommended:**
- PostgreSQL 12+ or MySQL 8+
- Alembic (for migrations)
- python-jose (for JWT)
- passlib (for password hashing)
- pytest (for testing)

## Quick Commands

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Run with custom host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Create migration
alembic revision --autogenerate -m "Add users table"

# Run migrations
alembic upgrade head

# Run tests
pytest

# Format code
black app/

# Type checking
mypy app/
```

## Resources

**Official Documentation:**
- [FastAPI Official Docs](https://fastapi.tiangolo.com)
- [FastAPI GitHub](https://github.com/tiangolo/fastapi)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)

**Local Documentation:**
- Complete examples: `references/examples.md`
- Project structure: `references/project-structure.md`
- Installation guide: `references/installation.md`
- Configuration: `references/configuration.md`
- Database setup: `references/database-setup.md`
- Authentication: `references/authentication.md`
- Troubleshooting: `references/troubleshooting.md`

**External Resources:**
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Real World FastAPI](https://github.com/nsidnev/fastapi-realworld-example-app)
- [Awesome FastAPI](https://github.com/mjhea0/awesome-fastapi)

## Version History

**v1.0.0 (2026-01-01)**
- Initial release
- Project scaffolding with standard structure
- SQLAlchemy database integration
- Pydantic schemas and validation
- Router organization patterns
- Dependency injection setup
- JWT authentication guide
- CRUD operation examples
- Migration setup with Alembic
- Complete reference documentation
- Context7 MCP integration

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Set PYTHONPATH or run with python -m
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python -m uvicorn app.main:app --reload
```

**Database Connection Failed:**
```bash
# Check DATABASE_URL in .env
# Verify database is running
sudo systemctl status postgresql
```

**Tables Not Found:**
```bash
# Create tables
python scripts/init_db.py
# Or run migrations
alembic upgrade head
```

**422 Validation Error:**
- Check request body matches Pydantic schema exactly
- Ensure all required fields are included

See `references/troubleshooting.md` for complete guide.

## Support

- [FastAPI GitHub Issues](https://github.com/tiangolo/fastapi/issues)
- [Stack Overflow - FastAPI Tag](https://stackoverflow.com/questions/tagged/fastapi)
- [FastAPI Discord](https://discord.gg/VQjSZaeJmf)
- [FastAPI Gitter](https://gitter.im/tiangolo/fastapi)

## Contributing

Improvements welcome! Please ensure:
- SKILL.md stays under 500 lines
- Examples are complete and tested
- Documentation follows progressive disclosure
- Code examples are production-ready

## License

This skill integrates with:
- FastAPI (MIT License)
- SQLAlchemy (MIT License)
- Pydantic (MIT License)

---

**Created with:** Claude Code + skill-creator + Context7 MCP
**Documentation Quality:** Production-ready
**Maintenance:** Self-contained, version 1.0.0
