from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import engine
from contextlib import contextmanager
from src.config import settings
import os
import logging
import time
from typing import Generator
from sqlalchemy import text

# Configure logging
logger = logging.getLogger(__name__)

# Import all models to ensure they are registered with SQLModel metadata before creating tables
from src.models.user import User  # noqa: F401
from src.models.task import Task  # noqa: F401


def get_engine(max_retries: int = 3, retry_delay: float = 1.0):
    """Create database engine with PostgreSQL configuration and retry logic"""
    database_url = settings.database_url

    if not database_url:
        logger.error("DATABASE_URL environment variable is not set")
        raise ValueError("DATABASE_URL environment variable is not set")

    # Attempt to create engine with retry logic
    last_exception = None
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})")

            # Create database engine with PostgreSQL configuration
            engine = create_engine(
                database_url,
                echo=True,
                pool_pre_ping=True,  # Verify connections before use
                pool_recycle=300,    # Recycle connections every 5 minutes
                pool_size=10,        # Number of connection pools
                max_overflow=20,     # Additional connections beyond pool_size
                pool_timeout=30,     # Timeout for getting connection from pool
                pool_reset_on_return='commit'  # Reset connections when returned to pool
            )

            # Test the connection
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            logger.info("Database engine created successfully")
            return engine

        except Exception as e:
            last_exception = e
            logger.warning(f"Database connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff

    logger.error(f"All {max_retries} database connection attempts failed. Last error: {str(last_exception)}")
    raise last_exception


def create_db_and_tables():
    """Create database tables if they don't exist with error handling"""
    try:
        logger.info("Starting database table creation...")
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise


def get_session() -> Generator[Session, None, None]:
    """Get database session with proper context management and error handling"""
    try:
        session = Session(engine)
        logger.debug("Database session created")
        yield session
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        try:
            session.close()
            logger.debug("Database session closed")
        except Exception as e:
            logger.error(f"Error closing database session: {str(e)}")


def validate_connection():
    """Validate that the database connection is working"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection validated successfully")
        return True
    except Exception as e:
        logger.error(f"Database connection validation failed: {str(e)}")
        return False


# Create database engine with error handling
try:
    engine = get_engine()
except Exception as e:
    logger.error(f"Failed to initialize database engine: {str(e)}")
    raise