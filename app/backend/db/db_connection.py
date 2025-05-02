import os
from typing import Generator
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

os.makedirs('data', exist_ok=True)

# Create engine
SQLALCHEMY_DATABASE_URL = "sqlite:///data/library.db"

# Create engine with SQLite connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create declarative base
Base = declarative_base()

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session() -> Generator[Session, None, None]:
    logger.debug("Opening new database session")
    db_session = SessionLocal()
    try:
        yield db_session
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise
    finally:
        logger.debug("Closing database session")
        db_session.close()