from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from api.schemas.metadata import LibraryMetadata

class IndexTypes(str, Enum):
    FlatL2 = 'flatl2'
    IVFIndex = 'ivf'

class AddLibraryRequest(BaseModel):
    name: str
    metadata: Optional[LibraryMetadata] = None
    
class LibraryResponseMessage(BaseModel):
    message: str = Field(default="Library added successfully, index built successfully, etc.")
    
class UpdateLibraryRequest(BaseModel):
    library_name: str
    new_name: str
    metadata: Optional[LibraryMetadata] = None
    
class QueryLibraryRequest(BaseModel):
    library_name: str
    query: str
    k: int
    
class ResponseLibrary(BaseModel):
    name: str = Field(default="library_name")
    metadata: LibraryMetadata