from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.tasks import router as tasks_router
from .api.health import router as health_router
from .api.auth import router as auth_router
from .database.connection import create_db_and_tables, validate_connection
from .config import settings
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Todo API", description="Task management API with JWT authentication", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(tasks_router)
app.include_router(health_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Backend API is running. Frontend handles the UI at root route."}

@app.on_event("startup")
def on_startup():
    """Initialize database tables on startup with comprehensive validation"""
    logger.info("Starting application initialization...")

    # Validate essential environment configuration
    if not settings.database_url:
        logger.critical("DATABASE_URL environment variable is not set!")
        raise ValueError("DATABASE_URL environment variable is required")

    if not settings.secret_key:
        logger.critical("SECRET_KEY environment variable is not set!")
        raise ValueError("SECRET_KEY environment variable is required")

    # Log warnings for non-critical but important configurations
    if not settings.better_auth_secret:
        logger.warning("BETTER_AUTH_SECRET environment variable is not set. Authentication may not work properly.")

    try:
        logger.info("Validating database connection...")
        # Test database connection before initializing tables
        if validate_connection():
            logger.info("Database connection validated successfully")
        else:
            logger.critical("Database connection validation failed!")
            raise ConnectionError("Unable to establish database connection")

        logger.info("Creating database tables...")
        create_db_and_tables()
        logger.info("Database tables initialized successfully.")

        logger.info("Application started successfully")

    except Exception as e:
        logger.critical(f"Failed to initialize application: {str(e)}")
        # In production, you might want to handle this differently
        # For now, we'll let the application fail to start
        raise

@app.on_event("shutdown")
def on_shutdown():
    """Cleanup on shutdown"""
    logger.info("Shutting down application...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)