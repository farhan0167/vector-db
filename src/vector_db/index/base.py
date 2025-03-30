from typing import List
from ..chunk import Chunk

class BaseIndex:
    def __init__(self):
        pass
    
    def add(self):
        pass
    
    def update(self):
        pass
    
    def remove(self):
        pass
    
    def search(self):
        pass
    
    def build_index(self):
        pass
    
class BaseVectorSearchIndex(BaseIndex):
    def __init__(self):
        self.chunks: List[Chunk] = []
        
    def get_chunks(self):
        return self.chunks