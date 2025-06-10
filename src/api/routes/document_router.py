import json
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..dependency import get_library, get_db
from api.schemas import AddDocumentRequest, ResponseDocument, LibraryResponseMessage

from vector_db import Library, Document, Database
from exceptions import DuplicateError

router = APIRouter()

@router.get("/document")
async def get_documents(
    library: Library = Depends(get_library)
):
    """Method to get all documents from a library"""
    try:
        docs = library.get_documents()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    response = [doc.dict() for doc in docs]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response
    )

@router.get("/document/{doc_id}")
async def get_document(
    doc_id: str, 
    library: Library = Depends(get_library)
):
    """Method to get a document from a library by its id"""
    try:
        doc = library.get_document(id=doc_id)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=doc.dict()
    )
    
@router.post("/document")
async def add_document(
    request: AddDocumentRequest, 
    db: Database = Depends(get_db)
):
    """Method to add a document to a library"""
    try:
        library = db.get_library(name=request.library_name)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    try:
        doc = library.add_document(
            document=Document(
                name=request.name,
                metadata=request.metadata.dict()
            )
        )
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=doc.dict()
    )
    

@router.delete("/document/{doc_id}")
async def remove_document(
    doc_id: str, 
    library: Library = Depends(get_library)
):
    """Remove a document from a library"""
    try:
        library.remove_document(id=doc_id)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return LibraryResponseMessage(
        message="Document removed successfully"
    )