# Database Schema Design with SQLModel

A comprehensive Claude Code skill for designing type-safe database schemas and managing migrations using SQLModel—combining SQLAlchemy's ORM with Pydantic's validation for FastAPI-compatible database layers.

## Overview

SQLModel is a library that bridges the gap between SQLAlchemy and Pydantic, allowing you to define database models that work seamlessly with FastAPI while providing automatic validation and type safety. This skill covers schema design, relationships, migrations with Alembic, and best practices.

## Features

### ✅ Type-Safe Models
- Combine SQLAlchemy ORM with Pydantic validation
- Full type hints and editor autocomplete
- Automatic data validation
- Single model for database and API

### ✅ Relationships
- One-to-many relationships
- Many-to-many with link tables
- Bidirectional relationships with back_populates
- Extra fields on link tables

### ✅ Database Operations
- CRUD operations
- Complex queries with filters
- Joins and aggregations
- Bulk operations
- Session management

### ✅ FastAPI Integration
- Same models for DB and API endpoints
- Automatic request/response validation
- Dependency injection patterns
- Separate read/write models

### ✅ Migrations
- Alembic integration
- Autogenerate migrations from models
- Schema version control
- Safe database evolution

## Installation

### Prerequisites

- Python 3.7+
- SQLModel (`pip install sqlmodel`)
- Alembic for migrations (`pip install alembic`)
- Database (PostgreSQL, MySQL, or SQLite)

### Skill Installation

```bash
# Copy to project skills
cp -r database-schema-sqlmodel /path/to/project/.claude/skills/

# Or copy to global skills
cp -r database-schema-sqlmodel ~/.claude/skills/
```

## Usage

### Activation

The skill activates with trigger keywords:
- "sqlmodel"
- "database schema"
- "sqlmodel relationships"
- "alembic migrations"
- "database models"
- "many-to-many sqlmodel"

### Quick Start

**Create a basic model:**
```python
from sqlmodel import Field, SQLModel, create_engine, Session

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = None

# Setup database
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

# Create and save
with Session(engine) as session:
    hero = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    session.add(hero)
    session.commit()
```

### Example Prompts

**Model Creation:**
- "Create SQLModel for users with validation"
- "Design database schema with SQLModel"
- "Add indexes to SQLModel fields"

**Relationships:**
- "Create one-to-many relationship in SQLModel"
- "Implement many-to-many with link table"
- "Add bidirectional relationships"

**Migrations:**
- "Set up Alembic with SQLModel"
- "Create migration for new table"
- "Handle schema evolution"

**FastAPI:**
- "Integrate SQLModel with FastAPI"
- "Create CRUD endpoints with SQLModel"
- "Separate read/write models"

## Documentation Structure

```
database-schema-sqlmodel/
├── SKILL.md (460 lines)          # Main workflow
├── README.md                      # This file
├── references/
│   ├── examples.md                # Complete implementations
│   ├── installation.md            # Setup guide
│   ├── database-setup.md          # Engine and session
│   ├── field-types.md             # Field configurations
│   ├── relationships.md           # Relationship patterns
│   ├── crud-operations.md         # Database operations
│   ├── fastapi-integration.md     # FastAPI patterns
│   ├── alembic-setup.md           # Migration setup
│   └── troubleshooting.md         # Common issues
├── assets/
│   └── templates/
│       └── alembic.ini            # Alembic config
└── scripts/
    └── init-sqlmodel.sh           # Quick setup
```

## Key Concepts

### Models vs Tables

**Table Model** (with `table=True`):
```python
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
```

**Schema Model** (without `table=True`):
```python
class HeroCreate(SQLModel):
    name: str
```

### Relationships

**One-to-Many:**
```python
class Team(SQLModel, table=True):
    heroes: list["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    team_id: int = Field(foreign_key="team.id")
    team: Team = Relationship(back_populates="heroes")
```

**Many-to-Many:**
```python
class HeroTeamLink(SQLModel, table=True):
    hero_id: int = Field(foreign_key="hero.id", primary_key=True)
    team_id: int = Field(foreign_key="team.id", primary_key=True)

class Hero(SQLModel, table=True):
    teams: list["Team"] = Relationship(link_model=HeroTeamLink)
```

### FastAPI Integration

```python
from fastapi import FastAPI, Depends
from sqlmodel import Session

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/heroes/")
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    return db_hero
```

## Common Use Cases

### Type-Safe Database Layer
Define models once, use for both database and API with full type checking

### FastAPI Backend
Build REST APIs with automatic validation and documentation

### Schema Migration
Manage database evolution with Alembic autogenerated migrations

### Complex Relationships
Model real-world data with one-to-many and many-to-many relationships

### Data Validation
Leverage Pydantic validation for database fields

## Best Practices

1. **Use table=True** - Only on models that represent database tables
2. **Type everything** - Use full type hints for editor support
3. **Define indexes** - Add `index=True` to frequently queried fields
4. **Use relationships** - Leverage back_populates for bidirectional access
5. **Separate concerns** - Different models for create/read/update
6. **Migrate safely** - Always use Alembic for schema changes
7. **Close sessions** - Use context managers (`with Session()`)
8. **Handle optionals** - Use `T | None` for nullable fields

## Integration with Other Skills

### With scaffolding-fastapi
- SQLModel as database layer for FastAPI
- Shared dependency injection patterns
- CRUD endpoint implementation
- Migration management

### With better-auth-nextjs
- Backend database models for users
- Session management
- Auth token storage

See `references/integration-guides.md` for detailed workflows (when created).

## Requirements

**Minimum:**
- Python 3.7+
- SQLModel 0.0.8+
- SQLAlchemy 2.0.0+
- Pydantic 2.0.0+

**Recommended:**
- FastAPI 0.100.0+ (for API integration)
- Alembic 1.11.0+ (for migrations)
- PostgreSQL 12+ or MySQL 8+ (for production)

## Quick Commands

```bash
# Install SQLModel
pip install sqlmodel alembic

# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Create tables"

# Run migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## Resources

**Official Documentation:**
- [SQLModel Official Docs](https://sqlmodel.tiangolo.com)
- [SQLModel GitHub](https://github.com/tiangolo/sqlmodel)
- [FastAPI SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Alembic Documentation](https://alembic.sqlalchemy.org)

**Local Documentation:**
- Complete examples: `references/examples.md`
- Installation guide: `references/installation.md`
- Database setup: `references/database-setup.md`
- Field types: `references/field-types.md`
- Relationships: `references/relationships.md`
- CRUD operations: `references/crud-operations.md`
- FastAPI integration: `references/fastapi-integration.md`
- Alembic setup: `references/alembic-setup.md`

## Version History

**v1.0.0 (2026-01-01)**
- Initial release
- Basic model creation with table=True
- Field types and constraints
- One-to-many relationships
- Many-to-many with link tables
- CRUD operation patterns
- FastAPI integration guide
- Alembic migration setup
- Complete reference documentation
- Context7 MCP integration

## Troubleshooting

### Common Issues

**Table not created:**
- Ensure `table=True` is set
- Call `SQLModel.metadata.create_all(engine)`

**Relationship not working:**
- Add `back_populates` to both sides
- Use correct table name in `foreign_key`

**Circular import:**
- Use forward references with quotes: `list["Model"]`

**Migration not detecting changes:**
- Import all models in `alembic/env.py`
- Set `target_metadata = SQLModel.metadata`

See `references/troubleshooting.md` for complete guide.

## Support

- [SQLModel GitHub Issues](https://github.com/tiangolo/sqlmodel/issues)
- [SQLModel Discord](https://discord.gg/VQjSZaeJmf) (FastAPI server)
- [Stack Overflow - SQLModel Tag](https://stackoverflow.com/questions/tagged/sqlmodel)

## Contributing

Improvements welcome! Please ensure:
- SKILL.md stays under 500 lines
- Examples are complete and tested
- Documentation follows progressive disclosure
- Code examples use modern Python (3.10+) syntax

## License

This skill integrates with:
- SQLModel (MIT License)
- SQLAlchemy (MIT License)
- Pydantic (MIT License)
- FastAPI (MIT License)

---

**Created with:** Claude Code + skill-creator + Context7 MCP
**Documentation Quality:** Production-ready
**Maintenance:** Self-contained, version 1.0.0
