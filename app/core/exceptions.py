# core/exceptions.py
from fastapi import HTTPException, status


class InvalidIDException(HTTPException):
    def __init__(self, detail="Invalid ID format"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ResourceNotFoundException(HTTPException):
    def __init__(self, resource_name="Resource"):
        detail = f"{resource_name} not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
