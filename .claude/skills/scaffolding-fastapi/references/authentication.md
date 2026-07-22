# FastAPI Authentication Guide

## JWT Authentication Setup

### Install Dependencies

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

### Security Module

**app/core/security.py:**
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

### Token Schemas

**app/schemas/token.py:**
```python
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int | None = None
    username: str | None = None
```

### Authentication Endpoints

**app/api/auth.py:**
```python
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, User as UserSchema
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.email == user_in.email) | (User.username == user_in.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )

    # Create user
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login with username and password to get access token."""
    # Find user
    user = db.query(User).filter(User.username == form_data.username).first()

    # Verify credentials
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
```

### Protected Routes

**app/api/deps.py:**
```python
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
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
    """Verify current user is a superuser."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges"
        )
    return current_user
```

### Usage in Routes

```python
from typing import Annotated
from fastapi import Depends
from app.api.deps import get_current_active_user, get_current_superuser
from app.models.user import User

# Type alias for cleaner code
CurrentUser = Annotated[User, Depends(get_current_active_user)]
CurrentSuperuser = Annotated[User, Depends(get_current_superuser)]

@router.get("/me", response_model=UserSchema)
async def read_me(current_user: CurrentUser):
    """Get current user profile."""
    return current_user

@router.get("/admin-only")
async def admin_route(current_user: CurrentSuperuser):
    """Admin-only endpoint."""
    return {"message": "Admin access granted"}
```

## OAuth2 Integration

### Google OAuth2

```bash
pip install authlib httpx
```

**Configuration:**
```env
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
GOOGLE_REDIRECT_URI="http://localhost:8000/auth/google/callback"
```

**Implementation:**
```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')

    # Find or create user
    user = db.query(User).filter(User.email == user_info['email']).first()
    if not user:
        user = User(
            email=user_info['email'],
            username=user_info['email'].split('@')[0],
            hashed_password=get_password_hash(secrets.token_urlsafe(32))
        )
        db.add(user)
        db.commit()

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
```

## API Key Authentication

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    """Verify API key."""
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@router.get("/protected")
async def protected_route(api_key: str = Depends(verify_api_key)):
    return {"message": "Access granted with API key"}
```

## Refresh Tokens

**Extended Token Schema:**
```python
class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
```

**Create Refresh Token:**
```python
def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token (longer expiration)."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@router.post("/login", response_model=TokenPair)
async def login(...):
    # ... existing login logic ...

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Get new access token using refresh token."""
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found or inactive")

        new_access_token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": new_access_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
```

## Role-Based Access Control (RBAC)

### Models

```python
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    permissions = Column(ARRAY(String))  # PostgreSQL specific

    users = relationship("User", secondary="user_roles", back_populates="roles")

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id"))
)

# Update User model
roles = relationship("Role", secondary=user_roles, back_populates="users")
```

### Permission Checking

```python
from functools import wraps
from typing import List

def require_permissions(permissions: List[str]):
    """Decorator to require specific permissions."""
    async def permission_checker(current_user: User = Depends(get_current_active_user)):
        user_permissions = set()
        for role in current_user.roles:
            user_permissions.update(role.permissions)

        if not all(perm in user_permissions for perm in permissions):
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        return current_user

    return permission_checker

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_permissions(["user:delete"]))
):
    # Delete user logic
    pass
```

## Security Best Practices

1. **Strong Secret Keys** - Use `secrets.token_urlsafe(32)` to generate
2. **HTTPS Only** - Never send tokens over HTTP
3. **Short Expiration** - Keep access tokens short-lived (15-30 minutes)
4. **Refresh Tokens** - Use for long-term access
5. **Password Requirements** - Enforce strong passwords
6. **Rate Limiting** - Prevent brute force attacks
7. **Token Revocation** - Implement token blacklist if needed
8. **Audit Logging** - Log authentication events

## Testing Authentication

```python
# tests/test_auth.py
def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "username": "testuser", "password": "password123"}
    )
    assert response.status_code == 201
    assert "id" in response.json()

def test_login_success(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_route(client, auth_headers):
    response = client.get("/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
```
