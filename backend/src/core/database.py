"""Database connection and session management."""

from flask import Flask
from sqlalchemy import create_engine , text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from src.config import config

# Create declarative base for models
Base = declarative_base()

# Global database engine and session factory
engine = None
SessionLocal = None


def init_db(app: Flask) -> None:
    """
    Initialize database connection
    
    Args:
        app: Flask application instance
    """
    global engine, SessionLocal
    
    # Create database engine
    engine = create_engine(
        config.DATABASE_URI,
        pool_pre_ping=True,  # Verify connections before using
        echo=config.DEBUG,   # Log SQL queries in debug mode
    )
    
    # Create session factory
    SessionLocal = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    
    # Store session in app context
    app.config["db_session"] = SessionLocal
    
    # Test connection
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        app.logger.info(f"Successfully connected to database: {config.DB_NAME}")
    except Exception as e:
        app.logger.error(f"Failed to connect to database: {e}")
        raise


def get_db():
    """
    Get database session.
    
    Yields:
        Database session
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        SessionLocal.remove()


def check_db_health() -> tuple[bool, str]:
    """
    Check PostgreSQL connection health.
    
    Returns:
        Tuple of (is_healthy, message)
    """
    if engine is None:
        return False, "Database engine not initialized"
    
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "Connection successful"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"


def close_db():
    """Close database connection."""
    global engine, SessionLocal
    if SessionLocal:
        SessionLocal.remove()
    if engine:
        engine.dispose()

