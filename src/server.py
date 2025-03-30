from fastapi import FastAPI, Request, HTTPException
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from api.routes import (
    library_router,
    document_router,
    chunk_router
)

app = FastAPI(
    title="vector-db",
    version="0.1.0",
    description="""
## API Documentation for vector-db
    """,
    openapi_tags=[
        {
            "name": "Library",
            "description": "Library related methods.",
        },
        {
            "name": "Document",
            "description": "Document related methods."
        },
        {
            "name": "Chunk",
            "description": "Chunk related methods."
        }
    ]
)

app.include_router(library_router.router)
app.include_router(document_router.router)
app.include_router(chunk_router.router)