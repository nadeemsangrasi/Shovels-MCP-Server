# Docker Project Structure

## Common Patterns

### Pattern 1: Single Service

```
myapp/
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── src/
│   └── ...
├── package.json  # or requirements.txt
└── README.md
```

### Pattern 2: Multi-Service (Monorepo)

```
project/
├── .dockerignore
├── docker-compose.yml
├── .env.example
├── frontend/               # Frontend service
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── backend/                # Backend service
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
├── nginx/                  # Reverse proxy
│   ├── Dockerfile
│   └── nginx.conf
└── scripts/
    └── docker-entrypoint.sh
```

### Pattern 3: Advanced Structure

```
project/
├── .dockerignore
├── compose.yaml
├── compose.override.yaml
├── compose.prod.yaml
├── .env.example
├── .gitignore
│
├── docker/
│   ├── app/
│   │   ├── Dockerfile
│   │   └── nginx/
│   │       └── nginx.conf
│   └── db/
│       └── init-scripts/
│           └── 01-schema.sql
│
├── services/
│   ├── api/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── src/
│   │
│   ├── web/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── src/
│   │
│   └── worker/
│       ├── Dockerfile
│       ├── requirements.txt
│       └── src/
│
├── scripts/
│   ├── build.sh
│   ├── deploy.sh
│   └── entrypoint.sh
│
├── configs/
│   ├── nginx.conf
│   ├── prometheus.yml
│   └── grafana/
│
└── tests/
    └── integration/
```

### Pattern 4: Next.js Project

```
my-nextjs-app/
├── .dockerignore
├── Dockerfile
├── compose.yaml
├── compose.override.yaml
├── .env.example
├── .gitignore
├── public/
├── src/
│   └── app/
├── package.json
├── next.config.js
└── next-env.d.ts
```

### Pattern 5: FastAPI Project

```
my-fastapi-app/
├── .dockerignore
├── Dockerfile
├── compose.yaml
├── compose.override.yaml
├── .env.example
├── .gitignore
├── app/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   └── schemas/
├── tests/
├── requirements.txt
└── alembic.ini
```

### Pattern 6: Go Project

```
my-go-app/
├── .dockerignore
├── Dockerfile
├── compose.yaml
├── .env.example
├── .gitignore
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── config/
│   ├── handler/
│   └── service/
├── go.mod
└── go.sum
```

## Key Files Explained

### .dockerignore

```dockerignore
# Essential patterns for all projects
.git
.gitignore
*.log
.env
.env.*

# IDE
.vscode
.idea

# OS
.DS_Store
Thumbs.db

# Docker
Dockerfile
docker-compose*
.dockerignore

# Documentation
README.md
CHANGELOG.md

# Dependencies (add language-specific)
node_modules/
venv/
__pycache__/
*.egg-info/
.target/
```

### Dockerfile

```
project/
└── Dockerfile
```

Naming variations:
- `Dockerfile` (standard)
- `Dockerfile.prod` (production-specific)
- `docker/Dockerfile` (in docker directory)

### compose.yaml

```
project/
├── compose.yaml              # Base config
├── compose.override.yaml     # Development overrides
├── compose.prod.yaml         # Production overrides
├── compose.staging.yaml      # Staging overrides
└── .env.example              # Environment template
```

### Environment Files

```bash
# .env.example (committed to repo)
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379
API_KEY=
```

```bash
# .env (gitignored)
DATABASE_URL=postgresql://app:secret@db:5432/app
REDIS_URL=redis://redis:6379/0
API_KEY=your-secret-key
```

## Best Practices

1. **One Dockerfile per service** - Keeps builds focused
2. **docker/ directory** - Organize Docker-related files
3. **compose.override.yaml** - For local development only
4. **.env.example** - Document required variables
5. **.dockerignore** - Reduce build context
6. **Version control** - Commit Docker configs, ignore built images
