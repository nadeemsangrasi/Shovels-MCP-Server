# FastAPI Database Setup Guide

## SQLAlchemy Configuration

### Basic Setup

**app/db/base.py:**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    echo=settings.DB_ECHO  # Log SQL queries in development
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create base class for models
Base = declarative_base()
```

**app/db/session.py:**
```python
from typing import Generator
from sqlalchemy.orm import Session
from app.db.base import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.

    Yields:
        Database session that will be closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Usage in Endpoints

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

@router.get("/users/")
async def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

## Database Models

### Basic Model

**app/models/user.py:**
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User {self.username}>"
```

### Model with Relationships

**app/models/post.py:**
```python
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post {self.title}>"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")

    def __repr__(self):
        return f"<Comment on Post {self.post_id}>"
```

**Update User model:**
```python
# Add to User class
posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
```

## Relationship Types

### One-to-Many

```python
class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    # One author has many books
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    author_id = Column(Integer, ForeignKey("authors.id"))

    # Many books belong to one author
    author = relationship("Author", back_populates="books")
```

### Many-to-Many

```python
# Association table
book_tags = Table(
    "book_tags",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))

    # Many books have many tags
    tags = relationship("Tag", secondary=book_tags, back_populates="books")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    # Many tags belong to many books
    books = relationship("Book", secondary=book_tags, back_populates="tags")
```

### One-to-One

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))

    # One user has one profile
    profile = relationship("Profile", back_populates="user", uselist=False)


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    bio = Column(Text)

    # One profile belongs to one user
    user = relationship("User", back_populates="profile")
```

## Migrations with Alembic

### Setup Alembic

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic
```

### Configure Alembic

**alembic.ini:**
```ini
[alembic]
script_location = alembic
prepend_sys_path = .

# Database URL (can be overridden by env.py)
sqlalchemy.url = postgresql://user:password@localhost:5432/dbname
```

**alembic/env.py:**
```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import your models
from app.db.base import Base
from app.core.config import settings
from app.models.user import User
from app.models.post import Post, Comment

# Alembic Config object
config = context.config

# Override sqlalchemy.url with settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Create and Run Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Create users table"

# Review the generated migration file in alembic/versions/

# Run migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

## Database Initialization Script

**scripts/init_db.py:**
```python
from sqlalchemy.orm import Session
from app.db.base import engine, Base, SessionLocal
from app.models.user import User
from app.models.post import Post, Comment
from app.core.security import get_password_hash

def init_db():
    """Initialize database with tables and seed data."""
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin = User(
                email="admin@example.com",
                username="admin",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_superuser=True
            )
            db.add(admin)
            db.commit()
            print("Admin user created")
        else:
            print("Admin user already exists")

    finally:
        db.close()


if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Database initialized successfully!")
```

**Run:**
```bash
python scripts/init_db.py
```

## Query Patterns

### Basic Queries

```python
from sqlalchemy.orm import Session

# Get all users
users = db.query(User).all()

# Get one user by ID
user = db.query(User).filter(User.id == 1).first()

# Get user by email
user = db.query(User).filter(User.email == "user@example.com").first()

# Count users
count = db.query(User).count()

# Check if exists
exists = db.query(User).filter(User.email == "user@example.com").first() is not None
```

### Filtering

```python
# Multiple filters (AND)
users = db.query(User).filter(
    User.is_active == True,
    User.is_superuser == False
).all()

# OR condition
from sqlalchemy import or_

users = db.query(User).filter(
    or_(User.email == "user@example.com", User.username == "user")
).all()

# IN operator
user_ids = [1, 2, 3]
users = db.query(User).filter(User.id.in_(user_ids)).all()

# LIKE operator
users = db.query(User).filter(User.username.like("%admin%")).all()

# NULL check
users = db.query(User).filter(User.updated_at == None).all()
```

### Ordering and Pagination

```python
# Order by
users = db.query(User).order_by(User.created_at.desc()).all()

# Pagination
page = 1
page_size = 10
users = db.query(User).offset((page - 1) * page_size).limit(page_size).all()

# Combined
users = db.query(User)\
    .filter(User.is_active == True)\
    .order_by(User.created_at.desc())\
    .offset(0)\
    .limit(10)\
    .all()
```

### Joins

```python
# Inner join
posts_with_authors = db.query(Post).join(User).all()

# Join with filter
posts = db.query(Post)\
    .join(User)\
    .filter(User.username == "admin")\
    .all()

# Eager loading (N+1 problem solution)
from sqlalchemy.orm import joinedload

posts = db.query(Post).options(joinedload(Post.author)).all()

# Access author without additional query
for post in posts:
    print(post.author.username)  # No extra query
```

### Aggregation

```python
from sqlalchemy import func

# Count posts by user
post_counts = db.query(
    User.username,
    func.count(Post.id).label("post_count")
).join(Post).group_by(User.id).all()

# Average, min, max
avg_post_length = db.query(func.avg(func.length(Post.content))).scalar()
min_date = db.query(func.min(Post.created_at)).scalar()
max_date = db.query(func.max(Post.created_at)).scalar()
```

## CRUD Operations

### Create

```python
# Single record
user = User(
    email="new@example.com",
    username="newuser",
    hashed_password=get_password_hash("password")
)
db.add(user)
db.commit()
db.refresh(user)  # Get updated fields (e.g., ID, timestamps)

# Multiple records
users = [
    User(email=f"user{i}@example.com", username=f"user{i}")
    for i in range(10)
]
db.add_all(users)
db.commit()
```

### Read

```python
# Get by primary key
user = db.query(User).get(1)

# Get with filter
user = db.query(User).filter(User.email == "user@example.com").first()

# Get or 404
from fastapi import HTTPException, status

user = db.query(User).filter(User.id == user_id).first()
if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
```

### Update

```python
# Update single field
user = db.query(User).filter(User.id == 1).first()
user.email = "newemail@example.com"
db.commit()
db.refresh(user)

# Update multiple fields
user = db.query(User).filter(User.id == 1).first()
for key, value in update_data.items():
    setattr(user, key, value)
db.commit()

# Bulk update
db.query(User).filter(User.is_active == False).update({"is_active": True})
db.commit()
```

### Delete

```python
# Delete single record
user = db.query(User).filter(User.id == 1).first()
db.delete(user)
db.commit()

# Bulk delete
db.query(User).filter(User.is_active == False).delete()
db.commit()
```

## Transactions

```python
from sqlalchemy.exc import IntegrityError

try:
    # Multiple operations in one transaction
    user = User(email="user@example.com", username="user")
    db.add(user)
    db.flush()  # Get user.id without committing

    profile = Profile(user_id=user.id, bio="User bio")
    db.add(profile)

    db.commit()  # Commit both operations
except IntegrityError:
    db.rollback()  # Rollback if any operation fails
    raise
```

## Connection Pooling

```python
from sqlalchemy import create_engine

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=5,              # Number of connections to keep open
    max_overflow=10,          # Max connections above pool_size
    pool_timeout=30,          # Seconds to wait for available connection
    pool_recycle=3600,        # Recycle connections after 1 hour
    pool_pre_ping=True,       # Verify connections before using
    echo=False                # Don't log SQL queries
)
```

## Best Practices

1. **Always use sessions properly** - Use dependency injection and `try/finally`
2. **Avoid N+1 queries** - Use `joinedload()` or `selectinload()`
3. **Use indexes** - Add `index=True` to frequently queried columns
4. **Use migrations** - Never modify models without creating migrations
5. **Handle exceptions** - Catch `IntegrityError`, `DataError`, etc.
6. **Use connection pooling** - Configure appropriate pool sizes
7. **Close sessions** - Always close or use context managers
8. **Validate before commit** - Use Pydantic schemas for validation

## Troubleshooting

### Issue: "No such table" error

**Solution:**
```bash
# Create tables
python scripts/init_db.py

# Or run migrations
alembic upgrade head
```

### Issue: DetachedInstanceError

**Solution:**
```python
# Enable expire_on_commit=False
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Keep objects accessible after commit
)
```

### Issue: Circular import with relationships

**Solution:**
```python
# Use string references
class Post(Base):
    author = relationship("User", back_populates="posts")  # String reference
```
