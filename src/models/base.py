"""
Shared SQLAlchemy Declarative Base.
All database models inherit from this base to allow centralized metadata collection.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
