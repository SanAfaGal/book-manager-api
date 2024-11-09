from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Query, Response
from starlette import status

from app.config.db import db
from app.core.utils import serialize_doc, get_document_or_404, dict_to_xml
from app.entities.author import Author, AuthorInDB

name_router = 'authors'
author_router = APIRouter(prefix=f'/{name_router}', tags=[name_router])
cursor = db.get_collection(name_router)


@author_router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_author(author: Author):
    """
    Create a new author in the database.

    **Requires**: An `Author` object containing the author's details.
    **Returns**: A dictionary with the newly created author's ID.

    - **Status Code 201**: Author created successfully.
    - **Status Code 422**: Invalid input validation error.
    """
    try:
        result = cursor.insert_one(author.dict())
        document_id = result.inserted_id
        return {"_id created": str(document_id)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error creating author: {str(e)}")


@author_router.get("/{author_id}", status_code=status.HTTP_200_OK)
async def get_author_by_id(author_id: str, format: str = Query("json", enum=["json", "xml"])):
    """
    Retrieve an author by their ID.

    **Requires**: A valid `author_id`.
    **Returns**: The author's details.

    - **Status Code 200**: Author found and returned.
    - **Status Code 400**: Invalid ID format.
    - **Status Code 404**: Author not found.
    """

    # Retrieve author from database
    author = get_document_or_404(cursor, author_id, "Author")

    # Serialize document
    author_data = serialize_doc(author, AuthorInDB).dict()

    # Return response in the specified format
    if format == "xml":
        author_data_xml = dict_to_xml("Author", author_data)
        return Response(content=author_data_xml, media_type="application/xml")

    # Return serialized author document
    return author_data


@author_router.get("/", status_code=status.HTTP_200_OK)
async def get_authors(skip: int = 0, limit: int = 10, format: str = Query("json", enum=["json", "xml"])):
    """
    Retrieve a list of authors with pagination.

    **Requires**: `skip` (offset) and `limit` (number of results) for pagination.
    **Returns**: A list of authors.

    - **Status Code 200**: Authors list returned successfully.
    - **Status Code 500**: Server error while retrieving authors.
    """
    try:
        authors = cursor.find().skip(skip).limit(limit)
        author_list = [serialize_doc(author, AuthorInDB).dict() for author in authors]

        if format == "xml":
            # Convert each author dict to XML
            authors_data_xml = "<Authors>"
            for author_data in author_list:
                authors_data_xml += dict_to_xml("Author", author_data)
            authors_data_xml += "</Authors>"
            return Response(content=authors_data_xml, media_type="application/xml")

        return author_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving authors: {str(e)}")


@author_router.put("/{author_id}", response_model=AuthorInDB, status_code=status.HTTP_200_OK)
async def update_author(author_id: str, author: Author):
    """
    Update an author's details.

    **Parameters**:
    - **author_id** (str): Unique ID of the author to be updated.
    - **author** (Author): Object containing the new details of the author.

    **Returns**:
    - **AuthorInDB**: Updated author data.

    **Status Codes**:
    - **200 OK**: Author updated successfully.
    - **404 Not Found**: Author with the given ID not found.
    - **500 Internal Server Error**: Error occurred while updating the author.
    """
    try:

        # Attempt to update the author
        cursor.update_one({"_id": ObjectId(author_id)}, {"$set": author.dict()})

        # Retrieve the updated author
        updated_author = cursor.find_one({"_id": ObjectId(author_id)})

        # Return the updated author
        return serialize_doc(updated_author, AuthorInDB)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error updating author: {str(e)}")


@author_router.delete("/{author_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_author(author_id: str):
    """
    Delete an author by their ID.

    **Parameters**:
    - **author_id** (str): Unique ID of the author to be deleted.

    **Returns**:
    - A message indicating the result of the operation.

    **Status Codes**:
    - **200 OK**: Author deleted successfully.
    - **404 Not Found**: Author with the given ID not found.
    """
    try:

        # Attempt to delete the author
        cursor.delete_one({"_id": ObjectId(author_id)})

        return {"detail": "Author deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error deleting author: {str(e)}")
