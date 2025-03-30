from fastapi import HTTPException, status
from vector_db import Database, Library

db = Database()

async def get_db() -> Database:
    return db

async def get_library(library_name: str) -> Library:
    try:
        library = db.get_library(name=library_name)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return library