from pydantic_settings import BaseSettings
from typing import Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    database_url: Optional[str] = None  # Will be set from environment variable
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    better_auth_secret: Optional[str] = None
    postgres_uri: Optional[str] = None  # Added to match environment variable

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Log important configuration warnings after initialization
        if not self.database_url:
            logger.critical("DATABASE_URL environment variable is not set!")
        else:
            logger.info("Database URL is configured")

        if not self.secret_key:
            logger.critical("SECRET_KEY environment variable is not set!")
        else:
            # Don't log the actual secret key for security
            logger.info("Secret key is configured")

        if not self.better_auth_secret:
            logger.warning("BETTER_AUTH_SECRET environment variable is not set. Authentication may not work properly.")
        else:
            logger.info("Better Auth secret is configured")

settings = Settings()