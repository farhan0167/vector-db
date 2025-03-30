from pydantic import BaseModel
from typing import Optional, List
from api.schemas.metadata import ChunkMetadata

class Chunk(BaseModel):
    text: str
    metadata: Optional[ChunkMetadata]

class AddChunkRequest(BaseModel):
    library_name: str
    chunks: List[Chunk] 
    
class UpdateChunkRequest(BaseModel):
    text: str