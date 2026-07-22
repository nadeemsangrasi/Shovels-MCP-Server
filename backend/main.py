"""
Shovels MCP Server — Main Application Entry Point

FastAPI application with FastMCP integration for the Shovels public API.
Provides 4 MCP tools for AI agents to search permits, contractors,
decisions, and resolve geo_ids.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

    # Verify Shovels API key is configured
    from src.config.settings import settings
    if not settings.SHOVELS_API_KEY:
        logger.warning("SHOVELS_API_KEY is not set — server will be non-functional")
    else:
        logger.info(
            "Shovels API configured",
            extra={"base_url": settings.SHOVELS_API_BASE},
        )

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
