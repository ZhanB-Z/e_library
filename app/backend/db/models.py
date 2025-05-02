# app/backend/db/models.py
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.types import TypeDecorator
import uuid
from .db_connection import Base

class UUIDType(TypeDecorator):
    """SQLite-compatible UUID type"""
    impl = BLOB
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return value.bytes
        
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return uuid.UUID(bytes=value)

class BookModel(Base):
    __tablename__ = "books"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year_published = Column(Integer, nullable=True)
    year_read = Column(Integer, nullable=True)
    cover_image_path = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)
    genres = Column(String, nullable=True)  # Comma-separated string
    cover_image = Column(String, nullable=True)
    is_remote_image = Column(Boolean, default=False)
    