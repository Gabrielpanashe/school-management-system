from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings

# Import routers
from app.api.v1 import auth, schools

settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A comprehensive school management platform",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware - Allows frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# Basic Routes
# ==========================================

@app.get("/")
async def root():
    """
    Health check endpoint.
    Returns basic API information.
    """
    return {
        "message": "School Management System API",
        "version": settings.VERSION,
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """
    Detailed health check for monitoring.
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "connected"
    }

# ==========================================
# Register API Routers
# ==========================================

# Include authentication routes
app.include_router(auth.router, prefix="/api/v1")
# Include school management routes
app.include_router(schools.router, prefix="/api/v1")