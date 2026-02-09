from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

# Create database engine
# echo=True means it will print SQL queries (useful for debugging)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,  # Check connection before using
    pool_size=10,        # Number of connections to maintain
    max_overflow=20      # Max extra connections if pool is full
)

# Session factory - creates database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()

def get_db():
    """
    Dependency that provides a database session.
    Automatically closes session after request.
    
    Usage in FastAPI:
    @app.get("/students")
    def get_students(db: Session = Depends(get_db)):
        ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()