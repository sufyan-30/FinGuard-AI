"""FastAPI application factory with CORS, database, and Redis"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
import pytz
import logging
import os

from backend.database import init_db, close_db, health_check as db_health
from backend.core import get_redis, redis_health_check
from backend.models import HealthCheckResponse
from backend.routers import vendors_router, invoices_router, audit_logs_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown event handlers"""
    logger.info("Starting up FastAPI application")
    await init_db()
    yield
    logger.info("Shutting down FastAPI application")
    await close_db()


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""

    app = FastAPI(
        title="FinGuard AI API",
        description="Enterprise fintech platform for vendor risk management",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS Configuration
    allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health Check Endpoint
    @app.get("/health", response_model=HealthCheckResponse)
    async def health_check(redis = Depends(get_redis)):
        """Health check endpoint with database and Redis status"""
        db_status = await db_health()
        redis_status = await redis_health_check()

        return HealthCheckResponse(
            status="healthy" if db_status["status"] == "healthy" and redis_status["status"] == "healthy" else "degraded",
            db=db_status["db"],
            redis=redis_status["redis"],
            timestamp=datetime.now(pytz.UTC),
        )

    # Register routers
    app.include_router(vendors_router)
    app.include_router(invoices_router)
    app.include_router(audit_logs_router)

    logger.info("FastAPI application created successfully")
    return app


app = create_app()
