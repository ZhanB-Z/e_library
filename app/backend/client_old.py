import json
import os
from typing import List, Optional
import uuid
from loguru import logger

from app.models.models import BookSchema

class BackendClient:
    """
    Template of the Backend Client 
    Used for data stored in .json file
    """
    def __init__(self, data_file: str = "books.json"):
        self.data_file = data_file
        # self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self) -> None:
        """Create the data file if it doesn't exist"""
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                    json.dump([], f)

    def get_book(self, book_id: uuid.UUID) -> Optional[BookSchema]:
        """Get a book by ID"""
        books = self.get_all_books()
        for book in books:
            if book.id == book_id:
                return book
        return None

    def add_book(self, book: BookSchema) -> BookSchema:
        """Add a new book to the storage"""
        books = self.get_all_books()
        books.append(book)
        self._save_books(books)
        return book
        
    def update_book(self, book: BookSchema) -> Optional[BookSchema]:
        """Update an existing book"""
        books = self.get_all_books()
        updated = False
        
        for i, existing_book in enumerate(books):
            if str(existing_book.id) == str(book.id):
                books[i] = book
                updated = True
                break
        if updated:
            self._save_books(books)
            return book
        return None
    
    def delete_book(self, bookd_id: uuid.UUID) -> bool:
        """Delete a book by ID"""
        books = self.get_all_books()
        initial_count = len(books)
        books = [book for book in books if str(book.id) != str(bookd_id)]
        
        if len(books) < initial_count:
            self._save_books(books)
            return True
        return False

    def _save_books(self, books: List[BookSchema]):
        """Save books to storage"""
        books_data = [book.model_dump() for book in books]
        with open(self.data_file, "w") as f:
            json.dump(books_data, f, indent=2, default=str)


def get_backend_client() -> BackendClient:
    return BackendClient()
