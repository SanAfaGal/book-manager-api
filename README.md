# Book Manager API

A FastAPI-based CRUD application designed to manage authors and their books, supporting both JSON and XML formats. The application connects to MongoDB Atlas for storage, providing efficient handling of book data.

## Features
- **CRUD operations** for authors and books
- **Support for JSON and XML formats**
- Integration with **MongoDB Atlas** for data storage

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/SanAfaGal/book-manager-api.git
    ```
2. **Create a virtual environment** and install packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Ensure you have the MongoDB Atlas connection string in the .env file:
   ```
   MONGODB_URI=
   MONGODB_DATABASE=
   ```
4. Run the application:
    ```bash
    uvicorn main:app --reload
    ```
## Make sure to
- Include your IP address in the IP access list by selecting the Network Access tab.
- Create a user and password to access the database.
- Update the correct username and password in the MONGODB_URI environment variable.

## Technologies
- FastAPI
- MongoDB Atlas
- Pydantic
- Python 3.x

## Usage and Examples
To view the documentation and test the endpoints, go to the following URL once the project is running:
```
http://127.0.0.1:8000/docs
```