import json
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..dependency import get_library, get_db

from vector_db import Library, Database, Chunk, ChunkMetadata
from api.schemas import AddChunkRequest

router = APIRouter()

@router.get("/chunk/{id}", summary="Get a chunk from a library", tags=["Chunk"])
async def get_chunk(id: str, library: Library = Depends(get_library)):
    try:
        chunk = library.get_chunk(chunk_id=id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=chunk.dict()
    )

@router.post("/chunk", summary="Add chunks to a library", tags=["Chunk"])
async def add_chunk(request: AddChunkRequest, db: Database = Depends(get_db)):
    library = db.get_library(name=request.library_name)
    chunks = []
    for chunk in request.chunks:
        chunks.append(
            Chunk(
                text=chunk.text,
                metadata=ChunkMetadata(
                    doc_id=chunk.doc_id,
                    page_number=chunk.page_number,
                    summary=chunk.summary
                ).dict()
            )
        )
    library.add_chunks(chunks=chunks)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Chunk added to library"}
    )

@router.delete("/chunk/{id}", summary="Remove a chunk from a library", tags=["Chunk"])
async def remove_chunk(id: str, library: Library = Depends(get_library)):
    pass