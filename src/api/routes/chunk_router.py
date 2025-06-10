import json
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from ..dependency import get_library, get_db

from vector_db import Library, Database, Chunk
from api.schemas import (
    AddChunkRequest, 
    UpdateChunkRequest, 
    ResponseChunk,
    LibraryResponseMessage
)
from exceptions import DuplicateError

router = APIRouter()

@router.get("/chunk")
async def get_chunks(
    document_id: Optional[str] = None, 
    library: Library = Depends(get_library)
):
    """Get all chunks from a library. If document_id is provided, then get all chunks from that document"""
    if document_id:
        try:
            doc = library.get_document(id=document_id)
            chunks_iter = doc.get_chunks()
        except KeyError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
    else:
        chunks_iter = library.get_chunks()
    chunks = [chunk.dict() for chunk in chunks_iter]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=chunks
    )

@router.get("/chunk/{id}")
async def get_chunk(
    id: str, 
    library: Library = Depends(get_library)
):
    """Method to get a chunk from a library by its id"""
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

@router.post("/chunk")
async def add_chunk(
    request: AddChunkRequest, 
    db: Database = Depends(get_db)
):
    """Method to add a chunk to a library"""
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
    return LibraryResponseMessage(
        message="Chunks added successfully"
    )
    
@router.patch("/chunk/{id}")
async def update_chunk(
    id: str, request: UpdateChunkRequest, 
    library: Library = Depends(get_library)
):
    """Update a chunk text from a library"""
    try:
        library.update_chunk(chunk_id=id, text=request.text)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return LibraryResponseMessage(
        message="Chunk updated successfully"
    )

@router.delete("/chunk/{id}")
async def remove_chunk(
    id: str, 
    library: Library = Depends(get_library)
):
    """Remove a chunk from a library"""
    try:
        library.remove_chunk(chunk_id=id)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return LibraryResponseMessage(
        message="Chunk removed successfully"
    )