from fastapi import FastAPI, Request, HTTPException
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from api.routes import (
    library_router,
    document_router,
    chunk_router
)

app = FastAPI()

app.include_router(library_router.router)
app.include_router(document_router.router)
app.include_router(chunk_router.router)