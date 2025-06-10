import json
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..dependency import get_db, get_library as get_library_

from api.schemas import (
    AddLibraryRequest,
    LibraryResponseMessage,
    IndexTypes as RequestIndexTypes,
    QueryLibraryRequest,
    UpdateLibraryRequest,
    ResponseLibrary,
    ResponseChunk
)
from vector_db import Database, Library
from exceptions import DuplicateError

router = APIRouter()

@router.get("/library")
async def get_libraries(
    db: Database = Depends(get_db)
):
    """
    Retrieve all libraries from the database.
    """
    libraries = db.get_libraries()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[library.dict() for library in libraries]
    )

@router.get("/library/{name}")
async def get_library(
    name: str, 
    db: Database = Depends(get_db)
):
    """
    Retrieve a library by its name from the database.
    """
    try:
        library = db.get_library(name)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=library.dict()
    )

@router.post("/library")
async def add_library(
    library: AddLibraryRequest, 
    index_type: RequestIndexTypes, 
    db: Database = Depends(get_db)
):
    """Add a library to the database."""
    try:
        lib = db.add_library(
            Library(**library.dict())
        )
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    lib.add_vector_search_index(index_type)
    
    return LibraryResponseMessage(
            message="Library added successfully"
    )
    
@router.patch("/library")
async def update_library(
    request: UpdateLibraryRequest, 
    db: Database = Depends(get_db)
):
    """Update a library's name in the database."""
    try:
        db.get_library(request.library_name)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    try:
        db.update_library_name(
            previous_name=request.library_name,
            new_name=request.new_name
        )
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    return LibraryResponseMessage(
        message="Library updated successfully"
    )

@router.delete("/library/{name}")
async def remove_library(
    name: str, 
    db: Database = Depends(get_db)
):
    """Remove a library from the database."""
    try:
        db.remove_library(name)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return LibraryResponseMessage(
        message="Library removed successfully"
    )

#-------------------Query-----------------------------------------------------------------------------

@router.patch("/library/query")
async def build_index(
    library: Library = Depends(get_library_)
):
    """Build the library's vector search index. Do this only when you have added all your chunks to the library."""
    try:
        library.build_index()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return LibraryResponseMessage(
        message="Index built successfully"
    )

@router.post("/library/query")
async def query(
    request: QueryLibraryRequest, 
    db: Database = Depends(get_db)
):
    """Perform a search on a library to retrieve relevant chunks."""
    try:
        library = db.get_library(name=request.library_name)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    try:
        results = library.search(query=request.query, k=request.k)
        chunks = [chunk.dict() for chunk in results]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=chunks
    )