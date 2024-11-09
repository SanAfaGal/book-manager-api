from typing import Optional

from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, example="Harry Potter and the Philosopher's Stone")
    author: str = Field(..., example="614d1a9c1a92386b7d123456")  # ObjectId as string
    genre: str = Field(..., min_length=2, max_length=50, example="Fantasy")
    published_year: int = Field(..., ge=1450, le=2024, example=1997)  # Year range validation
    pages: int = Field(..., gt=0, example=223)  # Positive integer validation
    summary: Optional[str] = Field(None, example="A young boy discovers he is a wizard on his 11th birthday.")


class BookInDB(Book):
    id: Optional[str] = Field(alias="_id")
