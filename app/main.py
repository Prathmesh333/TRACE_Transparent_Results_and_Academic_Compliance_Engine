"""
Opti-Scholar: Main FastAPI Application
Entry point for the API server
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.config import settings
from app.api.routes import documents, grading, verification, prediction, management, auth, data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}")
    # CSV Service doesn't need explicit init, just file checks which happen on access
    yield
    # Shutdown
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Intelligent Academic Assessment & Student Success Platform",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(grading.router, prefix="/api/v1/grades", tags=["Grading"])
app.include_router(verification.router, prefix="/api/v1/verification", tags=["Verification"])
app.include_router(prediction.router, prefix="/api/v1/prediction", tags=["Prediction"])
app.include_router(management.router, prefix="/api/v1", tags=["Management"])
app.include_router(data.router, prefix="/api/v1", tags=["Data"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "components": {
            "database": "connected",
            "gemini": "configured" if settings.gemini_api_key else "not_configured",
            "storage": "ready"
        }
    }


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "Intelligent Academic Assessment & Student Success Platform",
        "docs": "/docs",
        "health": "/health"
    }
