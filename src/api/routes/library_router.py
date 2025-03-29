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
from exceptions import DuplicateError

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

@router.post("/library", summary="Add a library", tags=["Library"])
async def add_library(library: AddLibraryRequest, index_type: RequestIndexTypes, db: Database = Depends(get_db)):
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
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=AddLibraryResponse(
            message="Library removed successfully"
        ).dict()
    )

#-------------------Query-----------------------------------------------------------------------------

@router.patch("/library/query", summary="Build the library's vector search index", tags=["Library"])
async def build_index(library: Library = Depends(get_library_)):
    try:
        library.build_index()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Index built successfully"}
    )

@router.post("/library/query", summary="Query a library", tags=["Library"])
async def query(request: QueryLibraryRequest, db: Database = Depends(get_db)):
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