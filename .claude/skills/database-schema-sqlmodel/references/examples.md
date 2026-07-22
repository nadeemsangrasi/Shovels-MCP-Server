# SQLModel Complete Examples

## Example 1: Basic Hero Model

### Simple Model with Fields
```python
from sqlmodel import Field, SQLModel, create_engine, Session

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

# Database setup
sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, echo=True)

# Create tables
SQLModel.metadata.create_all(engine)

# Create and save a hero
with Session(engine) as session:
    hero = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", age=16)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    print(f"Created hero: {hero}")
```

## Example 2: One-to-Many Relationship

### Team with Many Heroes
```python
from sqlmodel import Field, Relationship, SQLModel

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = None
    team_id: int | None = Field(default=None, foreign_key="team.id")

    team: Team | None = Relationship(back_populates="heroes")

# Usage
with Session(engine) as session:
    team = Team(name="Preventers", headquarters="Sharp Tower")
    hero1 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", team=team)
    hero2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", team=team)

    session.add(team)
    session.commit()
    session.refresh(team)

    print(f"Team: {team.name}")
    print(f"Heroes: {[h.name for h in team.heroes]}")
```

## Example 3: Many-to-Many Relationship

### Heroes and Teams with Link Table
```python
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

class HeroTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    teams: list[Team] = Relationship(back_populates="heroes", link_model=HeroTeamLink)

# Create and associate
with Session(engine) as session:
    team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
    team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

    hero_deadpond = Hero(
        name="Deadpond",
        secret_name="Dive Wilson",
        teams=[team_z_force, team_preventers],
    )

    session.add(hero_deadpond)
    session.commit()
    session.refresh(hero_deadpond)

    print(f"Deadpond teams: {[t.name for t in hero_deadpond.teams]}")
```

## Example 4: Many-to-Many with Extra Fields

### Link Table with Additional Data
```python
class HeroTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)
    is_training: bool = False  # Extra field

    team: "Team" = Relationship(back_populates="hero_links")
    hero: "Hero" = Relationship(back_populates="team_links")

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    hero_links: list[HeroTeamLink] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_links: list[HeroTeamLink] = Relationship(back_populates="hero")

# Access extra fields
with Session(engine) as session:
    hero = session.get(Hero, 1)
    for link in hero.team_links:
        print(f"{hero.name} -> {link.team.name}, Training: {link.is_training}")
```

## Example 5: FastAPI Integration

### Complete FastAPI App with SQLModel
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Models
class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: int | None = None

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class HeroCreate(HeroBase):
    pass

class HeroRead(HeroBase):
    id: int

class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None

# Database
sqlite_url = "sqlite:///./database.db"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# FastAPI app
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/heroes/", response_model=HeroRead)
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.get("/heroes/", response_model=list[HeroRead])
def read_heroes(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    heroes = session.exec(select(Hero).offset(skip).limit(limit)).all()
    return heroes

@app.get("/heroes/{hero_id}", response_model=HeroRead)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(hero_id: int, hero: HeroUpdate, session: Session = Depends(get_session)):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)

    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()
    return {"ok": True}
```

## Example 6: Querying with Filters

### Complex Queries
```python
from sqlmodel import select, func, or_, and_

with Session(engine) as session:
    # Simple filter
    statement = select(Hero).where(Hero.age >= 18)
    adults = session.exec(statement).all()

    # Multiple conditions (AND)
    statement = select(Hero).where(
        Hero.age >= 18,
        Hero.name.contains("Spider")
    )
    results = session.exec(statement).all()

    # OR conditions
    statement = select(Hero).where(
        or_(Hero.name == "Deadpond", Hero.age < 18)
    )
    results = session.exec(statement).all()

    # Join with relationship
    statement = select(Hero).join(Team).where(Team.name == "Preventers")
    heroes = session.exec(statement).all()

    # Aggregate
    statement = select(func.count(Hero.id))
    count = session.exec(statement).one()

    # Order and limit
    statement = select(Hero).order_by(Hero.age.desc()).limit(5)
    top_heroes = session.exec(statement).all()
```

## Example 7: Bulk Operations

### Efficient Batch Processing
```python
with Session(engine) as session:
    # Bulk insert
    heroes = [
        Hero(name=f"Hero {i}", secret_name=f"Secret {i}", age=20 + i)
        for i in range(100)
    ]
    session.add_all(heroes)
    session.commit()

    # Bulk update
    statement = select(Hero).where(Hero.age < 18)
    young_heroes = session.exec(statement).all()
    for hero in young_heroes:
        hero.age = 18
    session.commit()

    # Bulk delete
    statement = select(Hero).where(Hero.age > 100)
    old_heroes = session.exec(statement).all()
    for hero in old_heroes:
        session.delete(hero)
    session.commit()
```
