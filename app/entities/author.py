from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Author(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, example="J.K. Rowling")
    birthdate: datetime = Field(..., example=datetime(1965, 7, 31))
    nationality: str = Field(..., min_length=2, max_length=50, example="British")
    biography: Optional[str] = Field(None,
                                     example="J.K. Rowling is a British author, best known for the Harry Potter series.")


class AuthorInDB(Author):
    id: Optional[str] = Field(alias="_id")
