from pydantic import BaseModel
from typing import Optional

from api.schemas.metadata import DocumentMetadata

class AddDocumentRequest(BaseModel):
    name: str
    library_name: str
    metadata: Optional[DocumentMetadata]
    
class ResponseDocument(BaseModel):
    id: str
    name: str
    num_of_chunks: int
    metadata: Optional[DocumentMetadata]