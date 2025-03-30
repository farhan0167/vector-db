import datetime
from pydantic import BaseModel
from typing import Optional

class Metadata(BaseModel):
    date_created: str = "2025-01-01 00:00:00"
    
class LibraryMetadata(Metadata):
    description: Optional[str] = None
    
class DocumentMetadata(Metadata):
    source: Optional[str] = None
    
class ChunkMetadata(Metadata):
    doc_id: str
    page_number: Optional[int] = None
    summary: Optional[str] = None