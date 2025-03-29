import uuid
from typing import List, Dict, Any
from .chunk import Chunk

from utils.index import recompute_index

class Document:
    def __init__(
        self,
        name: str,
        metadata: Dict[str, Any]
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.chunks: List[Chunk] = []
        self.metadata = metadata
        self.__chunk_id_index: Dict[str, int] = {}
        
    def __repr__(self):
        return f"""Document(
            id='{self.id}', 
            name='{self.name}',
            chunks={self.chunks[:1]}...{self.chunks[-1:]},
            metadata={self.metadata}
        )""".strip()
        
    def get_name(self):
        return self.name
    
    
    def get_chunk(self, chunk_id: str):
        chunk_index = self.__chunk_id_index[chunk_id]
        return self.chunks[chunk_index]
    
    def add_chunk(self, chunk: Chunk):
        self.chunks.append(chunk)
        if chunk.id in self.__chunk_id_index:
            return
        self.__chunk_id_index[chunk.id] = len(self.chunks)-1
        
    def _update_chunk_text(
        self, 
        chunk_id: str, 
        text: str
    )-> Chunk:
        chunk_index = self.__chunk_id_index[chunk_id]
        chunk = self.chunks[chunk_index]
        chunk.text = text
        if chunk.embedding:
            pass
        return chunk
            
    def _remove_chunk(self, chunk_id: str):
        chunk_index = self.__chunk_id_index[chunk_id]
        del self.chunks[chunk_index]
        del self.__chunk_id_index[chunk_id]
        
        # Recompute chunk id index
        self.__chunk_id_index = recompute_index(
            iterable=self.chunks,
            key='id'
        )
    
    def get_chunks(self):
        return self.chunks
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "num_of_chunks": len(self.chunks),
            "metadata": self.metadata
        }
    
    
    
    