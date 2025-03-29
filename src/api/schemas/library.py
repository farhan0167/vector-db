from enum import Enum
from pydantic import BaseModel
from typing import Optional
from api.schemas.metadata import LibraryMetadata

class IndexTypes(str, Enum):
    FlatL2 = 'flatl2'

class AddLibraryRequest(BaseModel):
    name: str
    metadata: Optional[LibraryMetadata] = None
    
class AddLibraryResponse(BaseModel):
    message: str
    
class QueryLibraryRequest(BaseModel):
    library_name: str
    query: str
    k: int