from typing import List
from utils.embed import embed
from utils.knn import KNearNeighbors
from .base import BaseIndex, BaseVectorSearchIndex
from ..chunk import Chunk

class FlatL2Index(BaseVectorSearchIndex):
    """ 
    The FlatL2Index is a simple and rather brute force implementation of searching within
    a vector space. It's brute force because we're searching the entire vector space for any
    given query. This means that the search is a O(n) operation, where n is the number of
    chunks in library.
    """
    def __init__(self):
        super().__init__()
        self.embeddings: List[List[float]] = []
        self.knn_engine = None
        
    def add(self, chunks: List[Chunk]):
        for chunk in chunks:
            self.chunks.append(chunk)
            if not chunk.embedding:
                chunk.embedding = embed([chunk.text])[0]
            self.embeddings.append(chunk.embedding)
            
    def build_index(self):
        self.knn_engine = KNearNeighbors().fit(self.embeddings)
        
    def search(self, query, k):
        # embed the query
        query_embedding = embed([query])[0]
        # Get the k nearest neighbors
        neighbors = self.knn_engine.predict(query_embedding, k)
        # Get the chunks
        return [self.chunks[i] for i in neighbors]
        
    