import json
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..dependency import get_db, get_library as get_library_

from api.schemas import (
    AddLibraryRequest,
    AddLibraryResponse,
    IndexTypes as RequestIndexTypes,
    QueryLibraryRequest
)
from vector_db import Database, Library

router = APIRouter()

@router.get("/library", summary="Get all libraries", tags=["Library"])
async def get_libraries(db: Database = Depends(get_db)):
    libraries = db.get_libraries()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[library.dict() for library in libraries]
    )

@router.get("/library/{name}", summary="Get a library by name.", tags=["Library"])
async def get_library(name: str, db: Database = Depends(get_db)):
    return db.get_library(name)

@router.post("/library", summary="Add a library", tags=["Library"])
async def add_library(library: AddLibraryRequest, index_type: RequestIndexTypes, db: Database = Depends(get_db)):
    try:
        lib = db.add_library(
            Library(**library.dict())
        )
        lib.add_vector_search_index(index_type)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=AddLibraryResponse(
            message="Library added successfully"
        ).dict()
    )

@router.delete("/library/{name}", summary="Remove a library", tags=["Library"])
async def remove_library(name: str, db: Database = Depends(get_db)):
    try:
        db.remove_library(name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=AddLibraryResponse(
            message="Library removed successfully"
        ).dict()
    )

#-------------------Query-----------------------------------------------------------------------------

@router.patch("/library/query", summary="Build the library's vector search index", tags=["Library"])
async def build_index(library: Library = Depends(get_library_)):
    library.build_index()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Index built successfully"}
    )

@router.post("/library/query", summary="Query a library", tags=["Library"])
async def query(request: QueryLibraryRequest, db: Database = Depends(get_db)):
    library = db.get_library(name=request.library_name)
    results = library.search(query=request.query, k=request.k)
    chunks = [chunk.dict() for chunk in results]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=chunks
    )