# FastAPI Troubleshooting Guide

## Common Errors and Solutions

### Import Errors

#### Error: ModuleNotFoundError: No module named 'app'

**Cause:** Python can't find the `app` module

**Solutions:**
```bash
# Option 1: Run from project root
cd /path/to/my-api
python -m uvicorn app.main:app --reload

# Option 2: Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn app.main:app --reload

# Option 3: Add to .env or shell profile
echo 'export PYTHONPATH="${PYTHONPATH}:$(pwd)"' >> ~/.bashrc
```

#### Error: Circular import detected

**Cause:** Two modules import each other

**Solution:** Use forward references and import inside functions
```python
# Instead of
from app.models.user import User

# Use string reference in relationships
author = relationship("User", back_populates="posts")

# Or import inside functions
def get_user_posts(user_id: int):
    from app.models.post import Post
    return db.query(Post).filter(Post.author_id == user_id).all()
```

### Database Errors

#### Error: sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server

**Cause:** Database not running or wrong connection string

**Solutions:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Verify connection string in .env
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"

# Test connection
psql -U user -h localhost -d dbname
```

#### Error: sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedTable) relation "users" does not exist

**Cause:** Tables not created

**Solutions:**
```bash
# Option 1: Run initialization script
python scripts/init_db.py

# Option 2: Run migrations
alembic upgrade head

# Option 3: Create tables directly in Python
from app.db.base import Base, engine
Base.metadata.create_all(bind=engine)
```

#### Error: sqlalchemy.exc.IntegrityError: duplicate key value violates unique constraint

**Cause:** Trying to insert duplicate value in unique column

**Solution:** Check for existing records first
```python
existing_user = db.query(User).filter(User.email == email).first()
if existing_user:
    raise HTTPException(status_code=400, detail="User already exists")
```

### Pydantic Validation Errors

#### Error: 422 Unprocessable Entity

**Cause:** Request data doesn't match Pydantic schema

**Solution:** Check request body matches schema exactly
```python
# Schema expects
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

# Request must include all required fields
{
  "email": "user@example.com",
  "username": "user",
  "password": "password123"
}
```

#### Error: pydantic.error_wrappers.ValidationError: value is not a valid email address

**Cause:** Invalid email format

**Solutions:**
```bash
# Install email-validator
pip install email-validator

# Use EmailStr in schema
from pydantic import EmailStr

class User(BaseModel):
    email: EmailStr  # Validates email format
```

### Authentication Errors

#### Error: 401 Unauthorized - Could not validate credentials

**Causes & Solutions:**

**1. Token expired:**
```python
# Increase token expiration in .env
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**2. Wrong SECRET_KEY:**
```python
# Ensure SECRET_KEY matches between token creation and verification
# Check .env file
SECRET_KEY="same-key-everywhere"
```

**3. Token format incorrect:**
```bash
# Correct format in Authorization header
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Error: jose.exceptions.JWTError: Signature verification failed

**Cause:** SECRET_KEY mismatch or token tampered

**Solution:**
```python
# Regenerate token with correct SECRET_KEY
import secrets
secret_key = secrets.token_urlsafe(32)
print(f"SECRET_KEY={secret_key}")

# Update .env and restart server
```

### FastAPI Startup Errors

#### Error: RuntimeError: no validator found for <class 'pydantic_settings.sources.SecretsSettingsSource'>

**Cause:** Pydantic version mismatch

**Solution:**
```bash
# Upgrade pydantic and pydantic-settings
pip install --upgrade pydantic pydantic-settings

# Or specify compatible versions
pip install pydantic==2.6.0 pydantic-settings==2.6.0
```

#### Error: TypeError: Settings.__init__() got an unexpected keyword argument 'env_file'

**Cause:** Using old Pydantic BaseSettings API

**Solution:** Update to new API
```python
# Old (Pydantic v1)
class Settings(BaseSettings):
    class Config:
        env_file = ".env"

# New (Pydantic v2)
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
```

### CORS Errors

#### Error: Access to fetch at 'http://localhost:8000/api' from origin 'http://localhost:3000' has been blocked by CORS policy

**Solution:** Add CORS middleware
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Or ["*"] for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### File Upload Errors

#### Error: 413 Payload Too Large

**Cause:** Uploaded file exceeds server limit

**Solution:** Increase Nginx/proxy limit
```nginx
# nginx.conf
client_max_body_size 50M;
```

```python
# Or limit in FastAPI
from fastapi import UploadFile, File, HTTPException

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.size > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(status_code=413, detail="File too large")
```

### Performance Issues

#### Problem: Slow queries (N+1 problem)

**Cause:** Loading relationships in loops

**Solution:** Use eager loading
```python
# Bad: N+1 queries
posts = db.query(Post).all()
for post in posts:
    print(post.author.username)  # Queries for each post

# Good: Single query with join
from sqlalchemy.orm import joinedload

posts = db.query(Post).options(joinedload(Post.author)).all()
for post in posts:
    print(post.author.username)  # No extra queries
```

#### Problem: High memory usage

**Cause:** Loading too many records at once

**Solution:** Use pagination
```python
@app.get("/users")
async def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users
```

### Migration Errors

#### Error: Target database is not up to date

**Cause:** Alembic version mismatch

**Solutions:**
```bash
# Check current version
alembic current

# Check history
alembic history

# Upgrade to latest
alembic upgrade head

# Or downgrade and re-upgrade
alembic downgrade base
alembic upgrade head
```

#### Error: Can't locate revision identified by 'xyz'

**Cause:** Migration file missing or corrupted

**Solution:**
```bash
# Check alembic/versions/ directory
ls alembic/versions/

# Stamp database to specific version
alembic stamp head

# Or create new migration
alembic revision --autogenerate -m "Fix migration"
```

## Debugging Tips

### Enable SQL Logging

```python
# app/db/base.py
engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # Logs all SQL queries
)
```

### Enable FastAPI Debug Mode

```python
# app/main.py
app = FastAPI(debug=True)  # Detailed error messages
```

### Use Python Debugger

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use built-in breakpoint()
breakpoint()
```

### Check Uvicorn Logs

```bash
# Run with detailed logging
uvicorn app.main:app --reload --log-level debug

# Or save logs to file
uvicorn app.main:app --reload --log-config logging.conf
```

### Test Database Connection

```python
# scripts/test_db.py
from app.db.base import engine, SessionLocal
from sqlalchemy import text

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            print(f"Result: {result.fetchone()}")
    except Exception as e:
        print(f"Database connection failed: {e}")

    try:
        db = SessionLocal()
        result = db.execute(text("SELECT current_database()"))
        print(f"Connected to database: {result.fetchone()[0]}")
        db.close()
    except Exception as e:
        print(f"Session test failed: {e}")

if __name__ == "__main__":
    test_connection()
```

## Environment-Specific Issues

### Development

**Problem:** Hot reload not working

**Solution:**
```bash
# Ensure --reload flag is used
uvicorn app.main:app --reload

# Or install watchfiles for better file watching
pip install watchfiles
uvicorn app.main:app --reload --reload-dir app
```

### Production

**Problem:** Application crashes under load

**Solutions:**
```bash
# Use multiple workers
uvicorn app.main:app --workers 4

# Or use Gunicorn with Uvicorn workers
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Problem:** Database connection pool exhausted

**Solution:**
```python
# Increase pool size
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,  # Increase from default 5
    max_overflow=40,  # Increase from default 10
)
```

## Getting Help

### Useful Commands

```bash
# Check FastAPI version
python -c "import fastapi; print(fastapi.__version__)"

# Check installed packages
pip list

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Test endpoint directly
curl -X GET "http://localhost:8000/docs"

# Check environment variables
python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
```

### FastAPI Resources

- [Official Documentation](https://fastapi.tiangolo.com)
- [GitHub Issues](https://github.com/tiangolo/fastapi/issues)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/fastapi)
- [Discord Community](https://discord.gg/VQjSZaeJmf)

### SQLAlchemy Resources

- [Official Documentation](https://docs.sqlalchemy.org)
- [SQLAlchemy Discord](https://discord.gg/FyCp8z)

### Pydantic Resources

- [Official Documentation](https://docs.pydantic.dev)
- [GitHub Discussions](https://github.com/pydantic/pydantic/discussions)
