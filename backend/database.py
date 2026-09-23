"""
Database setup for MindBridge backend.
Uses SQLAlchemy with SQLite (default) or PostgreSQL (if DATABASE_URL is set).
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_ROOT, "data")
os.makedirs(_DATA_DIR, exist_ok=True)

DEFAULT_SQLITE_URL = f"sqlite:///{os.path.join(_DATA_DIR, 'mindbridge.db')}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

# Configure SQLite engine specifics (check_same_thread=False for multithreading in FastAPI)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency for database session management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
