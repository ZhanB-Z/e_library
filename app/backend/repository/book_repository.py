from loguru import logger
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.models import BookSchema
from app.backend.db.models import BookModel

class BookRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def create_book(self, book: BookSchema) -> BookSchema:
        """Adds a book to the db"""
        logger.info(f"REPOSITORY: CREATE_BOOK")
        db_book = self._convert_model_to_db(book=book)
        
        self.db_session.add(db_book)
        self.db_session.commit()
        self.db_session.refresh(db_book)
        
        return self._convert_db_to_model(db_book=db_book)

    def get_all_books(self) -> list[BookSchema]:
        """Retrieves all books from the database"""
        db_books = self.db_session.query(BookModel).all()
        return [self._convert_db_to_model(db_book=book) for book in db_books]
        
    def get_book_by_id(self, book_id: UUID) -> BookSchema:
        """Retrieves a book by its ID"""
        db_book = self.db_session.query(BookModel).filter(BookModel.id == book_id).first()
        if db_book:
            return self._convert_db_to_model(db_book=db_book)
        return None
        
    def update_book(self, book: BookSchema) -> BookSchema:
        """Updates an existing book in the database"""
        db_book = self.db_session.query(BookModel).filter(BookModel.id == book.id).first()
        if not db_book:
            return None
            
        # Convert model to DB and ensure we keep the same ID
        updated_db_book = self._convert_model_to_db(book=book)
        
        # Copy all attributes from updated model to existing model
        for key, value in vars(updated_db_book).items():
            if key != '_sa_instance_state':  # Skip SQLAlchemy internal attribute
                setattr(db_book, key, value)
        
        self.db_session.commit()
        self.db_session.refresh(db_book)
        
        return self._convert_db_to_model(db_book=db_book)
        
    def delete_book(self, book_id: UUID) -> bool:
        """Deletes a book from the database"""
        db_book = self.db_session.query(BookModel).filter(BookModel.id == book_id).first()
        if not db_book:
            return False
            
        self.db_session.delete(db_book)
        self.db_session.commit()
        
        return True

    
    def _convert_model_to_db(self, book: BookSchema) -> BookModel:
        """Convert Pydantic model to SQLAlchemy model"""
        # Convert genres list to comma-separated string
        genres_str = ",".join(book.genres) if book.genres else ""
        
        db_book = BookModel()
        db_book.id = book.id
        db_book.title = book.title
        db_book.author = book.author
        db_book.year_published = book.year_published
        db_book.year_read = book.year_read
        db_book.cover_image_path = book.cover_image_path
        db_book.summary = book.summary
        db_book.rating = book.rating
        db_book.genres = genres_str
        db_book.cover_image = book.cover_image
        db_book.is_remote_image = book.is_remote_image
        
        return db_book
    
    def _convert_db_to_model(self, db_book: BookModel) -> BookSchema:
        """Convert SQLAlchemy model to Pydantic model"""
        # Convert comma-separated genres string to list
        genres_list = []
        if db_book.genres:
            genres_list = [genre.strip() for genre in db_book.genres.split(",") if genre.strip()]
            
        return BookSchema(
            id=db_book.id,
            title=db_book.title,
            author=db_book.author,
            year_published=db_book.year_published,
            year_read=db_book.year_read,
            cover_image_path=db_book.cover_image_path,
            summary=db_book.summary,
            rating=db_book.rating,
            genres=genres_list,
            cover_image=db_book.cover_image,
            is_remote_image=db_book.is_remote_image
        )