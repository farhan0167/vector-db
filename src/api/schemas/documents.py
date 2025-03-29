from pydantic import BaseModel
from typing import Optional

from vector_db.metadata import DocumentMetadata

class AddDocumentRequest(BaseModel):
    name: str
    library_name: str
    metadata: Optional[DocumentMetadata]