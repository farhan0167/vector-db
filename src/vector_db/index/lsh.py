import random
from typing import List
from utils.embed import embed
from utils.knn import KNearNeighbors
from .base import BaseVectorSearchIndex
from .collections_index import CollectionsIndex
from ..chunk import Chunk

class LSHIndex(BaseVectorSearchIndex):
    def __init__(self):
        super().__init__()
        self.embeddings: List[List[float]] = []
        self.chunks_index = CollectionsIndex()
        self.hyperplanes = self.__generate_random_hyperplanes()
        self.buckets = {}
        
    def __generate_random_hyperplanes(self, n_planes=20, dim=1024):
        hyperplanes = []
        for _ in range(n_planes):
            plane = [random.gauss(0, 1) for _ in range(dim)]
            hyperplanes.append(plane)
        return hyperplanes
    
    def __hash(self, embedding, hyperplane):
        hash_bits = []
        for plane in hyperplane:
            dot = sum(e*p for e, p in zip(embedding, plane))
            hash_bits.append("1" if dot > 0 else "0")
        return "".join(hash_bits)
    
    def __hamming_distance(self, s1: str, s2: str):
        return sum(x != y for x, y in zip(s1, s2))
    
    def add(self, chunks: List[Chunk]):
        for chunk in chunks:
            self.chunks.append(chunk)
            chunk_index = len(self.chunks)-1
            if not chunk.embedding:
                chunk.embedding = embed([chunk.text])[0]
            self.embeddings.append(chunk.embedding)
            self.chunks_index.add(id=chunk.id, value=chunk_index)
            # Add to LSH Index
            key = self.__hash(chunk.embedding, self.hyperplanes)
            if key not in self.buckets:
                self.buckets[key] = []
            self.buckets[key].append(chunk.id)
            
    def search(self, query, k):
        # embed the query
        query_embedding = embed([query])[0]
        # Hash the query embedding
        key = self.__hash(query_embedding, self.hyperplanes)
        # Check to see if the key exists in the buckets
        search_space = self.buckets.get(key, [])
        if not search_space:
            # If no match was found, get the two nearest buckets
            n_probe = 2
            all_keys = list(self.buckets.keys())
            n_closest_keys = sorted(all_keys, key=lambda k: self.__hamming_distance(key, k))[:n_probe]
            for closest_key in n_closest_keys:
                search_space.extend(self.buckets[closest_key])
        # Tuple to store the embedding and chunk id
        embeddings_idx = [
            ( self.embeddings[ self.chunks_index.search(chunk_id) ], chunk_id ) 
            for chunk_id in search_space
        ]
        # Get the k nearest neighbors
        knn_engine = KNearNeighbors().fit([embedding for embedding, _ in embeddings_idx])
        neighbors = knn_engine.predict(query_embedding, k)
        # Get the chunks
        chunks = []
        for neighbor in neighbors:
            chunk_id = embeddings_idx[neighbor][1]
            chunks.append(
                self.chunks[ self.chunks_index.search(chunk_id) ]
            )
        return chunks
        
    def remove(self, chunk_id: str):
        chunk_index = self.chunks_index.search(chunk_id)
        del self.chunks[chunk_index]
        self.chunks_index.remove(
            id=chunk_id, 
            iterable=self.chunks, 
            reindex_key='id'
        )
        # Remove chunk from LSH Index
        key = self.__hash(self.embeddings[chunk_index], self.hyperplanes)
        self.buckets[key].remove(chunk_id)
        del self.embeddings[chunk_index]
        
    def update(self, chunk_id: str, text: str):
        chunk_index = self.chunks_index.search(chunk_id)
        # Remove chunk from LSH Index
        key = self.__hash(self.embeddings[chunk_index], self.hyperplanes)
        self.buckets[key].remove(chunk_id)
        # Update chunk
        self.chunks[chunk_index].text = text
        self.embeddings[chunk_index] = embed([text])[0]
        # Add chunk to LSH Index
        key = self.__hash(self.embeddings[chunk_index], self.hyperplanes)
        if key not in self.buckets:
            self.buckets[key] = []
        self.buckets[key].append(chunk_id)
        

