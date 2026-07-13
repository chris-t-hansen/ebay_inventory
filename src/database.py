"""
Database Connection and Session Management.
Uses SQLAlchemy to configure connection pools and handle transactions with MariaDB.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from src.config import Config

# Create the SQLAlchemy engine for MariaDB
# pool_recycle: Recycles connections after an hour to avoid 'MySQL server has gone away' errors
# pool_pre_ping: Checks if connection is alive before serving a query
engine = create_engine(
    Config.get_database_url(),
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=False,  # Set to True for verbose SQL logging during debugging
)

# Create a thread-safe local session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency / context manager to ensure database sessions are correctly closed after use."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_db_connection() -> bool:
    """Utility to verify that the database parameters are correct and a connection can be established."""
    try:
        with engine.connect() as connection:
            # Execute a lightweight native MariaDB command to verify connection
            from sqlalchemy import text
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection failure: {e}")
        return False
