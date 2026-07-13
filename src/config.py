"""
Configuration Loader Module.
Responsible for reading environment variables and providing them as structured configuration parameters.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Automatically locate the .env file in the project root
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    load_dotenv()


class Config:
    """Application configuration and credentials loader."""

    # MariaDB/MySQL Configuration
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "ebay_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "ebay_inventory")

    @classmethod
    def get_database_url(cls) -> str:
        """Returns the database connection URL formatted for SQLAlchemy using PyMySQL."""
        # Clean any special characters in the password or username if required by URL encoding
        return f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}?charset=utf8mb4"

    # eBay Developer Configuration
    EBAY_APP_ID: str | None = os.getenv("EBAY_APP_ID")
    EBAY_DEV_ID: str | None = os.getenv("EBAY_DEV_ID")
    EBAY_CERT_ID: str | None = os.getenv("EBAY_CERT_ID")
    EBAY_REDIRECT_URI: str | None = os.getenv("EBAY_REDIRECT_URI")
    
    # Must be 'sandbox' or 'production'
    EBAY_ENVIRONMENT: str = os.getenv("EBAY_ENVIRONMENT", "sandbox").lower()

    @classmethod
    def validate_ebay_credentials(cls) -> bool:
        """Helper to check if essential eBay API keys are provided."""
        return all([cls.EBAY_APP_ID, cls.EBAY_CERT_ID, cls.EBAY_REDIRECT_URI])
