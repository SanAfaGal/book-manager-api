from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.core.exceptions import InvalidIDException, ResourceNotFoundException
from app.routes.author_router import author_router

app = FastAPI(
    title="Book Management API",
    description="A FastAPI-based CRUD application designed to manage authors and their books, supporting both JSON and XML formats. The application connects to MongoDB Atlas for storage, providing efficient handling of book data."
)


@app.exception_handler(InvalidIDException)
async def invalid_id_exception_handler(request, exc: InvalidIDException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(ResourceNotFoundException)
async def resource_not_found_exception_handler(request, exc: ResourceNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.include_router(author_router)


@app.get('/')
def root():
    return {"message": "Go to http://127.0.0.1:8000/docs"}
