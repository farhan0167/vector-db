from typing import List
from ..chunk import Chunk

class BaseIndex:
    def __init__(self):
        self.chunks: List[Chunk] = []
        
    def get_chunks(self):
        return self.chunks
    
    def add(self):
        pass
    
    def search(self):
        pass
    
    def build_index(self):
        pass