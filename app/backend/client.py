# app/backend/client.py
from typing import List, Optional
from uuid import UUID

from app.models.models import BookSchema
from app.backend.db.db_connection import get_db_session, engine, Base
from app.backend.repository.book_repository import BookRepository

# Create tables when app starts
Base.metadata.create_all(bind=engine)

class BackendClient:
    def __init__(self):
        # Get a session from the session pool
        self.db = next(get_db_session())
        self.book_repository = BookRepository(db_session=self.db)
    
    def get_all_books(self) -> List[BookSchema]:
        """Retrieve all books from the database"""
        return self.book_repository.get_all_books()
    
    def get_book_by_id(self, book_id: UUID) -> Optional[BookSchema]:
        """Retrieve a specific book by ID"""
        return self.book_repository.get_book_by_id(book_id)
    
    def save_book(self, book: BookSchema) -> BookSchema:
        """Save or update a book"""
        existing_book = None
        if book.id:
            existing_book = self.get_book_by_id(book.id)
            
        if existing_book:
            # Update existing book
            return self.book_repository.update_book(book)
        else:
            # Create new book
            return self.book_repository.create_book(book)
    
    def delete_book(self, book_id: UUID) -> bool:
        """Delete a book by ID"""
        return self.book_repository.delete_book(book_id)

def get_backend_client() -> BackendClient:
    """Factory function to create a backend client"""
    return BackendClient()