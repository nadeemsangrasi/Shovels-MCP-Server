"""
Shovels MCP Server — Main Application Entry Point

FastAPI application with FastMCP integration for the Shovels public API.
Provides 4 MCP tools for AI agents to search permits, contractors,
decisions, and resolve geo_ids.
"""

from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.mcp.server import mcp
from src.mcp import tools  # Import to register tools
from src.utils.logger import setup_logging, get_logger

# Setup structured logging
setup_logging(level="INFO")
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Minimal startup — no Qdrant, no embedding models, no database.
    """
    logger.info("Starting Shovels MCP Server")

    # Note: SHOVELS_API_KEY is optional. Each request must include
    # X-API-Key header — keys are validated per-request via the
    # Shovels /usage endpoint and forwarded to all tool calls.
    from src.config.settings import settings
    logger.info("Shovels MCP Server starting", extra={"base_url": settings.SHOVELS_API_BASE})

    async with mcp.session_manager.run():
        yield

    logger.info("Shutting down Shovels MCP Server")


# Create FastAPI application
app = FastAPI(
    title="Shovels MCP Server",
    description="MCP server wrapping the Shovels public API — search permits, contractors, decisions, and resolve geo locations.",
    version="2.0.0",
    lifespan=lifespan,
)

# Add CORS middleware for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include health router
from src.api.health import router as health_router
app.include_router(health_router)

# Mount FastMCP at root path
app.mount("/", mcp.streamable_http_app())


# ── API Key Middleware ──────────────────────────────────────

# Simple in-memory cache of validated keys to avoid re-checking every request
_validated_keys: set[str] = set()


@app.middleware("http")
async def require_api_key(request: Request, call_next):
    """
    Require a valid X-API-Key header by checking it against the Shovels API.
    Makes a lightweight call to the /usage endpoint to validate the key.
    Results are cached in-memory so each key is only checked once.
    """
    # Skip auth for health checks and CORS preflight
    if request.url.path == "/health" or request.method == "OPTIONS":
        return await call_next(request)

    api_key = request.headers.get("X-API-Key")
    if not api_key:
        return JSONResponse(
            status_code=401,
            content={
                "error": "auth_error",
                "code": 2,
                "message": "Missing X-API-Key header. Get a key at https://app.shovels.ai",
            },
        )

    # Check cache first
    if api_key not in _validated_keys:
        # Validate against Shovels API
        from src.config.settings import settings

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{settings.SHOVELS_API_BASE}/usage",
                    headers={"X-API-Key": api_key},
                )

            if response.status_code == 401:
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": "auth_error",
                        "code": 2,
                        "message": "Invalid API key. Check your X-API-Key header.",
                    },
                )

            if response.status_code == 402:
                # Trial credit limit reached — surface the upgrade URL
                body = response.json()
                detail = body.get("detail", "Trial credit limit reached.")
                return JSONResponse(
                    status_code=402,
                    content={
                        "error": "credit_exhausted",
                        "code": 3,
                        "message": detail,
                    },
                )

            if response.status_code == 200:
                _validated_keys.add(api_key)
            else:
                # Unexpected status — log and reject
                logger.error(
                    "API key validation returned unexpected status",
                    extra={"status": response.status_code},
                )
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": "auth_error",
                        "code": 2,
                        "message": "Could not validate API key.",
                    },
                )

        except (httpx.ConnectError, httpx.TimeoutException) as e:
            # Shovels API unreachable — reject with 503
            logger.error(
                "Shovels API unreachable during key validation",
                extra={"error": str(e)},
            )
            return JSONResponse(
                status_code=503,
                content={
                    "error": "service_unavailable",
                    "code": 4,
                    "message": "Shovels API is unreachable. Try again later.",
                },
            )

    # Set the caller's key in the request context so tools use it
    from src.services.shovels_client import set_request_api_key
    set_request_api_key(api_key)

    return await call_next(request)


logger.info("FastMCP mounted at root path")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
