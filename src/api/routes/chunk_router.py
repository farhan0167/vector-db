import json
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..dependency import get_library, get_db

from vector_db import Library, Database, Chunk
from api.schemas import AddChunkRequest, UpdateChunkRequest
from exceptions import DuplicateError

router = APIRouter()

@router.get("/chunk", summary="Get all chunks by document from a library", tags=["Chunk"])
async def get_chunks(document_id: str, library: Library = Depends(get_library)):
    try:
        doc = library.get_document(id=document_id)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    chunks = [chunk.dict() for chunk in doc.get_chunks()]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=chunks
    )

@router.get("/chunk/{id}", summary="Get a chunk from a library", tags=["Chunk"])
async def get_chunk(id: str, library: Library = Depends(get_library)):
    try:
        chunk = library.get_chunk(chunk_id=id)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=chunk.dict()
    )

@router.post("/chunk", summary="Add chunks to a library", tags=["Chunk"])
async def add_chunk(request: AddChunkRequest, db: Database = Depends(get_db)):
    try:
        library = db.get_library(name=request.library_name)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    chunks = []
    for chunk in request.chunks:
        chunks.append(
            Chunk(
                text=chunk.text,
                metadata=chunk.metadata.model_dump()
            )
        )
    try:
        library.add_chunks(chunks=chunks)
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Chunk added to library"}
    )
    
@router.patch("/chunk/{id}", summary="Update a chunk text from a library", tags=["Chunk"])
async def update_chunk(id: str, request: UpdateChunkRequest, library: Library = Depends(get_library)):
    try:
        library.update_chunk(chunk_id=id, text=request.text)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Chunk updated successfully"}
    )

@router.delete("/chunk/{id}", summary="Remove a chunk from a library", tags=["Chunk"])
async def remove_chunk(id: str, library: Library = Depends(get_library)):
    try:
        library.remove_chunk(chunk_id=id)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Chunk removed successfully"}
    )