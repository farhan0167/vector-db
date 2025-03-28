import uuid
from typing import List
from .chunk import Chunk
from .metadata import DocumentMetadata

class Document:
    def __init__(
        self,
        name: str,
        metadata: DocumentMetadata
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.content = ''
        self.chunks: List[Chunk] = []
        self.metadata = metadata
        
    def __repr__(self):
        return f"""Document(
            id='{self.id}', 
            name='{self.name}', 
            content='{f'{self.content[:20].strip()}...{self.content[-20:].strip()}'}', 
            chunks={self.chunks[:1]}...{self.chunks[-1:]},
            metadata={self.metadata.model_dump()}
        )""".strip()
        
    def get_name(self):
        return self.name
    
    def get_text(self):
        return self.content
    
    def add_chunks(self, chunks: List[Chunk]):
        self.chunks.extend(chunks)
        for chunk in chunks:
            self.content+=chunk.text
    
    def get_chunks(self):
        return self.chunks
    
    
    
    