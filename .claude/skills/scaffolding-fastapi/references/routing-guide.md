# FastAPI Routing Guide

## Basic Routing

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def list_users():
    return {"users": []}

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

@router.post("/")
async def create_user():
    return {"message": "User created"}
```

## Path Parameters

```python
# Integer parameter
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# String parameter
@router.get("/users/{username}")
async def get_user_by_username(username: str):
    return {"username": username}

# Enum parameter
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

@router.get("/users/role/{role}")
async def get_users_by_role(role: UserRole):
    return {"role": role}
```

## Query Parameters

```python
@router.get("/users/")
async def list_users(skip: int = 0, limit: int = 10, search: str | None = None):
    return {"skip": skip, "limit": limit, "search": search}

# With validation
from pydantic import Field

@router.get("/users/")
async def list_users(
    skip: int = Field(default=0, ge=0),
    limit: int = Field(default=10, ge=1, le=100)
):
    return {"skip": skip, "limit": limit}
```

## Request Body

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

@router.post("/users/")
async def create_user(user: UserCreate):
    return {"username": user.username, "email": user.email}
```

## Response Models

```python
class User(BaseModel):
    id: int
    username: str
    email: str

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    return {"id": user_id, "username": "user", "email": "user@example.com", "password": "hidden"}
    # password field is excluded automatically
```

## Status Codes

```python
from fastapi import status

@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    return None
```

## Dependencies

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

@router.get("/users/")
async def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

## Router Organization

**app/main.py:**
```python
from fastapi import FastAPI
from app.api import users, posts, auth

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
```
