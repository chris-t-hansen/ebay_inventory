"""
Shared Pytest Fixtures and Configurations.
Configures an in-memory SQLite database specifically for testing database operations safely and quickly.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.models.base import Base


@pytest.fixture(scope="session")
def test_engine():
    """Creates a temporary SQLite in-memory database and creates all tables."""
    # Use SQLite in-memory for isolated, lightning-fast testing of models/relations
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_engine) -> Session:
    """Provides an isolated database session per test case, rolling back any modifications after completion."""
    connection = test_engine.connect()
    transaction = connection.begin()

    # Create session bound to the transaction connection
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
