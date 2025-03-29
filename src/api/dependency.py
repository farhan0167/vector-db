from vector_db import Database, Library

db = Database()

async def get_db() -> Database:
    return db

async def get_library(library_name: str) -> Library:
    return db.get_library(name=library_name)