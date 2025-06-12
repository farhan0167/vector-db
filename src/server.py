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
    version="0.1.0"
)

app.include_router(library_router.router, prefix="/api")
app.include_router(document_router.router, prefix="/api")
app.include_router(chunk_router.router, prefix="/api")