import uuid
from pydantic import BaseModel, Field
from typing import Optional, List

class Book(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    author: str
    year_published: Optional[int] = None
    year_read: Optional[int]
    cover_image_path: str
    summary: Optional[str]
    rating: Optional[int] = None
    genres: List[str] = []
    cover_image: Optional[str]
    is_remote_image: bool = False