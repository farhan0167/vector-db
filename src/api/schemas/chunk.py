from pydantic import BaseModel
from typing import Optional, List

class Chunk(BaseModel):
    text: str
    doc_id: str
    page_number: Optional[int]
    summary: Optional[str]

class AddChunkRequest(BaseModel):
    library_name: str
    chunks: List[Chunk]