---
name: database-schema-sqlmodel
description: Design database schemas and manage migrations with SQLModel. Use when creating type-safe database models, defining relationships (one-to-many, many-to-many), setting up Alembic migrations, integrating with FastAPI, and building Pydantic-compatible database layers with SQLAlchemy under the hood.
version: 1.0.0
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
author: Claude Code
tags: [sqlmodel, database, schema, migrations, alembic, fastapi, pydantic, sqlalchemy, relationships, orm]
---

# Database Schema Design with SQLModel

Design type-safe database schemas and manage migrations using SQLModel—combining the best of SQLAlchemy and Pydantic. Build FastAPI-compatible database layers with automatic validation and seamless ORM integration.

## Overview

SQLModel is a library that combines SQLAlchemy's ORM capabilities with Pydantic's validation, creating a unified way to define database models that work seamlessly with FastAPI. This skill covers schema design, relationships, migrations, and best practices.

## When to Use This Skill

**Activate when:**
- Designing database schemas from scratch
- Creating SQLModel models with table=True
- Defining relationships (one-to-many, many-to-many)
- Setting up database migrations with Alembic
- Converting SQLAlchemy models to SQLModel
- Building type-safe FastAPI database layers
- Managing database schema evolution

**Trigger keywords:** "sqlmodel", "database schema", "sqlmodel relationships", "alembic migrations", "database models", "many-to-many sqlmodel"

**NOT for:**
- Non-Python projects
- NoSQL databases
- Simple in-memory data structures
- Django ORM projects

## Prerequisites

**Required:**
- Python 3.7+
- SQLModel installed (`pip install sqlmodel`)
- Basic SQL and database knowledge
- Understanding of type hints

**Recommended:**
- FastAPI knowledge
- Pydantic familiarity
- Alembic for migrations (`pip install alembic`)
- PostgreSQL/MySQL/SQLite

## Instructions

### Phase 1: Basic Model Setup

#### Step 1: Install SQLModel

**Quick:**
```bash
pip install sqlmodel alembic
```

**See:** `references/installation.md`

#### Step 2: Create First Model

**Quick:**
```python
from sqlmodel import Field, SQLModel

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = None
```

**See:** `references/examples.md#basic-model`

#### Step 3: Create Database and Tables

**Quick:**
```python
from sqlmodel import create_engine, SQLModel

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)
```

**See:** `references/database-setup.md`

### Phase 2: Field Configuration

#### Step 4: Define Field Types

**Common patterns:**
```python
# Required field
name: str

# Optional field
age: int | None = None

# With default
is_active: bool = True

# Primary key
id: int | None = Field(default=None, primary_key=True)

# Indexed field
email: str = Field(index=True, unique=True)
```

**See:** `references/field-types.md`

#### Step 5: Add Field Constraints

**Quick:**
```python
from sqlmodel import Field

class User(SQLModel, table=True):
    email: str = Field(unique=True, index=True)
    age: int = Field(ge=0, le=150)
    name: str = Field(min_length=1, max_length=100)
```

**See:** `references/field-constraints.md`

### Phase 3: Relationships

#### Step 6: One-to-Many Relationship

**Quick:**
```python
from sqlmodel import Relationship

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    heroes: list["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    team_id: int | None = Field(foreign_key="team.id")

    team: Team | None = Relationship(back_populates="heroes")
```

**See:** `references/relationships.md#one-to-many`

#### Step 7: Many-to-Many Relationship

**Quick:**
```python
class HeroTeamLink(SQLModel, table=True):
    hero_id: int | None = Field(foreign_key="hero.id", primary_key=True)
    team_id: int | None = Field(foreign_key="team.id", primary_key=True)

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    teams: list["Team"] = Relationship(
        back_populates="heroes",
        link_model=HeroTeamLink
    )
```

**See:** `references/relationships.md#many-to-many`

### Phase 4: Database Operations

#### Step 8: Create Records

**Quick:**
```python
from sqlmodel import Session

with Session(engine) as session:
    hero = Hero(name="Spider-Boy", age=16)
    session.add(hero)
    session.commit()
    session.refresh(hero)
```

**See:** `references/crud-operations.md#create`

#### Step 9: Query Records

**Quick:**
```python
from sqlmodel import select

with Session(engine) as session:
    statement = select(Hero).where(Hero.age >= 18)
    heroes = session.exec(statement).all()
```

**See:** `references/crud-operations.md#read`

### Phase 5: FastAPI Integration

#### Step 10: FastAPI Endpoints

**Quick:**
```python
from fastapi import FastAPI, Depends
from sqlmodel import Session

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
```

**See:** `references/fastapi-integration.md`

### Phase 6: Migrations with Alembic

#### Step 11: Initialize Alembic

**Quick:**
```bash
alembic init alembic
```

**Configure `alembic/env.py`:**
```python
from sqlmodel import SQLModel
from your_app.models import *  # Import all models

target_metadata = SQLModel.metadata
```

**See:** `references/alembic-setup.md`

#### Step 12: Create and Run Migrations

**Quick:**
```bash
# Create migration
alembic revision --autogenerate -m "Create hero table"

# Run migration
alembic upgrade head
```

**See:** `references/migrations-guide.md`

### Phase 7: Advanced Patterns

#### Step 13: Separate Read/Write Models

**Quick:**
```python
class HeroBase(SQLModel):
    name: str
    age: int | None = None

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class HeroCreate(HeroBase):
    pass

class HeroRead(HeroBase):
    id: int
```

**See:** `references/model-patterns.md#read-write-separation`

#### Step 14: Handle Complex Queries

**Quick:**
```python
from sqlmodel import select, func

# Join query
statement = select(Hero, Team).join(Team)
results = session.exec(statement).all()

# Aggregate query
statement = select(func.count(Hero.id))
count = session.exec(statement).one()
```

**See:** `references/advanced-queries.md`

## Common Patterns

### Pattern 1: Basic CRUD Model
**Quick:** SQLModel with table=True + CRUD operations

**See:** `references/examples.md#crud-model`

### Pattern 2: One-to-Many Relationship
**Quick:** Foreign key + Relationship with back_populates

**See:** `references/relationships.md#one-to-many`

### Pattern 3: Many-to-Many with Link Table
**Quick:** Link model + Relationship with link_model parameter

**See:** `references/relationships.md#many-to-many`

### Pattern 4: Separate Read/Write Schemas
**Quick:** Base model + table model + create/read variants

**See:** `references/model-patterns.md#schemas`

### Pattern 5: Migration Workflow
**Quick:** Model changes → autogenerate → review → upgrade

**See:** `references/migrations-guide.md`

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No table generated | Missing `table=True` | Add `table=True` to class definition |
| Relationship not working | Missing back_populates | Add back_populates to both sides |
| Foreign key error | Wrong table name in foreign_key | Use lowercase table name |
| Migration conflicts | Manual schema changes | Always use Alembic for changes |
| Circular import | Models import each other | Use forward references with quotes |

**See:** `references/troubleshooting.md`

## SQLModel Features

**Type Safety:** Pydantic validation + SQLAlchemy ORM
**FastAPI Integration:** Same models for DB and API
**Automatic Validation:** Built-in data validation
**Editor Support:** Full autocomplete and type checking
**Simple Syntax:** Less boilerplate than SQLAlchemy

**See:** `references/features.md`

## Best Practices

1. **Use table=True** - Only for database tables, not for schemas
2. **Define indexes** - Add index=True to frequently queried fields
3. **Use relationships** - Leverage back_populates for bidirectional access
4. **Separate concerns** - Different models for create/read/update
5. **Type everything** - Full type hints for editor support
6. **Use migrations** - Always use Alembic for schema changes
7. **Handle None** - Use `Optional[T]` or `T | None` for nullable fields
8. **Close sessions** - Use context managers for sessions

## Validation Checklist

**Model Definition:**
- [ ] `table=True` for database models
- [ ] Primary key defined
- [ ] Foreign keys reference correct tables
- [ ] Indexes on frequently queried fields
- [ ] Type hints on all fields

**Relationships:**
- [ ] back_populates on both sides
- [ ] link_model for many-to-many
- [ ] Foreign keys match relationship
- [ ] Forward references (quotes) for circular deps

**Migrations:**
- [ ] Alembic initialized
- [ ] env.py configured with SQLModel.metadata
- [ ] All models imported in env.py
- [ ] Migrations reviewed before applying

**Integration:**
- [ ] FastAPI dependencies set up
- [ ] Session management correct
- [ ] Response models defined
- [ ] Error handling implemented

## Quick Reference

**Create Model:**
```python
class Model(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
```

**Create Engine:**
```python
engine = create_engine("sqlite:///db.db")
SQLModel.metadata.create_all(engine)
```

**Session:**
```python
with Session(engine) as session:
    # operations
```

**Query:**
```python
statement = select(Model).where(Model.field == value)
results = session.exec(statement).all()
```

**See:** `references/quick-reference.md`

## References

**Local Documentation:**
- Examples: `references/examples.md`
- Installation: `references/installation.md`
- Database setup: `references/database-setup.md`
- Field types: `references/field-types.md`
- Relationships: `references/relationships.md`
- CRUD operations: `references/crud-operations.md`
- FastAPI integration: `references/fastapi-integration.md`
- Alembic setup: `references/alembic-setup.md`
- Migrations guide: `references/migrations-guide.md`
- Troubleshooting: `references/troubleshooting.md`

**External Resources:**
- [SQLModel Official Docs](https://sqlmodel.tiangolo.com)
- [SQLModel GitHub](https://github.com/tiangolo/sqlmodel)
- [FastAPI SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)

## Tips for Success

1. **Start simple** - Basic model first, add complexity gradually
2. **Test relationships** - Verify back_populates works both ways
3. **Use type hints** - Enable full editor support
4. **Review migrations** - Always check autogenerated migrations
5. **Handle optionals** - Be explicit about None vs required
6. **Leverage Pydantic** - Use Field() for validation
7. **Close sessions** - Always use context managers
8. **Document models** - Add docstrings to complex models

## Version History

**v1.0.0 (2026-01-01)**
- Initial release
- Basic model creation
- Relationship patterns (one-to-many, many-to-many)
- Field types and constraints
- CRUD operations
- FastAPI integration
- Alembic migration setup
- Complete reference documentation
- Context7 MCP integration

## Sources

- [SQLModel Official Documentation](https://sqlmodel.tiangolo.com)
- [SQLModel on Context7](https://context7.com/websites/sqlmodel_tiangolo)
- SQLModel GitHub Repository
