from typing import TypeVar, Type
from xml.etree.ElementTree import Element, tostring

from bson import ObjectId
from pydantic import BaseModel

from app.core.exceptions import InvalidIDException, ResourceNotFoundException

# Define a generic type for Pydantic entities
ModelType = TypeVar("ModelType", bound=BaseModel)


# Generalized function to serialize MongoDB documents to Pydantic entities
def serialize_doc(doc: dict, model: Type[ModelType]) -> ModelType:
    # Convert ObjectId to string if "_id" is present in the document
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    # Create an instance of the given model with the document data
    return model(**doc)


def dict_to_xml(tag: str, data: dict) -> str:
    """
    Convert a dictionary to an XML string.

    **Parameters**:
    - **tag** (str): Root XML tag.
    - **data** (dict): Data to convert into XML format.

    **Returns**:
    - XML string representation of the data.
    """
    element = Element(tag)
    for key, val in data.items():
        child = Element(key)
        child.text = str(val)
        element.append(child)
    return tostring(element, encoding='utf-8').decode('utf-8')


def validate_object_id(id: str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise InvalidIDException()
    return ObjectId(id)


def get_document_or_404(collection, object_id: str, resource_name="Resource"):
    document = collection.find_one({"_id": validate_object_id(object_id)})
    if not document:
        raise ResourceNotFoundException(resource_name=resource_name)
    return document
