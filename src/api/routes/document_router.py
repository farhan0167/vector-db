import json
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..dependency import get_library, get_db
from api.schemas import AddDocumentRequest

from vector_db import Library, Document, Database

router = APIRouter()

@router.get("/document", summary="Get all documents from a library", tags=["Document"])
async def get_documents(library: Library = Depends(get_library)):
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

@router.get("/document/{doc_id}", summary="Get a document from a library", tags=["Document"])
async def get_document(doc_id: str, library: Library = Depends(get_library)):
    doc = library.get_document(id=doc_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=doc.dict()
    )
    
@router.post("/document", summary="Add a document to a library", tags=["Document"])
async def add_document(request: AddDocumentRequest, db: Database = Depends(get_db)):
    library = db.get_library(name=request.library_name)
    doc = library.add_document(
        document=Document(
            name=request.name,
            metadata=request.metadata.dict()
        )
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=doc.dict()
    )
    

@router.delete("/document/{doc_id}", summary="Remove a document a library", tags=["Document"])
async def remove_document(doc_id: str, library: Library = Depends(get_library)):
    pass