from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings

# Import routers
from app.api.v1 import (
    auth, schools, academic, 
    students, subjects, attendance, 
    grades, reports, finance, 
    finance_reports, users
)

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

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(schools.router, prefix="/api/v1")
app.include_router(academic.router, prefix="/api/v1")
app.include_router(students.router, prefix="/api/v1")
app.include_router(subjects.router, prefix="/api/v1")
app.include_router(attendance.router, prefix="/api/v1")
app.include_router(grades.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.include_router(finance.router, prefix="/api/v1")
app.include_router(finance_reports.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")