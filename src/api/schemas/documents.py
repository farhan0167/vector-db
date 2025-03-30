from pydantic import BaseModel
from typing import Optional

from api.schemas.metadata import DocumentMetadata

class AddDocumentRequest(BaseModel):
    name: str
    library_name: str
    metadata: Optional[DocumentMetadata]