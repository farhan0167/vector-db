import random
import math
from pydantic import BaseModel
from typing import List, Dict
from utils.embed import embed
from utils.knn import KNearNeighbors
from .collections_index import CollectionsIndex
from .base import BaseVectorSearchIndex
from ..chunk import Chunk


def euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

class Kmeans:
    """ 
    Disclaimer: This implementation is a product of vibe coding since I'm running out of time.
    The algorithm for fit, however, is one that I came up from my grad school ML class. Theoretically,
    I could've used the sklearn implementation if I needed to vibe code this.
    """
    
    def __init__(self, n_clusters=2, n_iter=10):
        self.n_clusters = n_clusters
        self.n_iter = n_iter

    def initialize_means(self, embeddings, k):
        dim = len(embeddings[0])
        mins = [min(dim_i) for dim_i in zip(*embeddings)]
        maxs = [max(dim_i) for dim_i in zip(*embeddings)]
        
        means = []
        for _ in range(k):
            mean = [random.uniform(mins[d], maxs[d]) for d in range(dim)]
            means.append(mean)
        return means

    def assign_clusters(self, embeddings, means):
        assignments = []
        for emb in embeddings:
            distances = [euclidean_distance(emb, mean) for mean in means]
            cluster_idx = distances.index(min(distances))
            assignments.append(cluster_idx)
        return assignments

    def update_means(self,embeddings, assignments, k):
        dim = len(embeddings[0])
        new_means = [[0.0] * dim for _ in range(k)]
        counts = [0] * k
        
        for emb, cluster_idx in zip(embeddings, assignments):
            counts[cluster_idx] += 1
            for d in range(dim):
                new_means[cluster_idx][d] += emb[d]
        
        for i in range(k):
            if counts[i] == 0:
                continue  # Avoid division by zero
            for d in range(dim):
                new_means[i][d] /= counts[i]
        return new_means

    def fit(self, embeddings):
        means = self.initialize_means(embeddings, self.n_clusters)
        
        for _ in range(self.n_iter):
            assignments = self.assign_clusters(embeddings, means)
            means = self.update_means(embeddings, assignments, self.n_clusters)
        
        return means, assignments
    
class ChunkEmbedding:
    def __init__(self, embedding: List[float], chunk: Chunk):
        self.embedding = embedding
        self.chunk = chunk

    
class IVFIndex(BaseVectorSearchIndex):
    def __init__(self):
        super().__init__()
        self.cluster_centers = []
        self.center_map = []
        self.index: Dict[int, List[ChunkEmbedding]] = {}
        self.embeddings: List[List[float]] = []
        self.chunks_index = CollectionsIndex()
        
    def add(self, chunks: List[Chunk]):
        for chunk in chunks:
            self.chunks.append(chunk)
            if not chunk.embedding:
                chunk.embedding = embed([chunk.text])[0]
            self.embeddings.append(chunk.embedding)
            self.chunks_index.add(id=chunk.id, value=len(self.chunks)-1)
            
    def remove(self, chunk_id: str):
        chunk_index = self.chunks_index.search(chunk_id)
        del self.chunks[chunk_index]
        del self.embeddings[chunk_index]
        self.chunks_index.remove(id=chunk_id, iterable=self.chunks, reindex_key='id')
        
    def update(self, chunk_id: str, text: str):
        chunk_index = self.chunks_index.search(chunk_id)
        self.chunks[chunk_index].text = text
        self.embeddings[chunk_index] = embed([text])[0]
        
    def build_index(self):
        self.cluster_centers, self.center_map = Kmeans(
            n_clusters=2,
            n_iter=100
        ).fit(self.embeddings)
        
        for i in range(len(self.cluster_centers)):
            self.index[i] = []
        
        for embedding_idx, cm in enumerate(self.center_map):
            self.index[cm].append(
                ChunkEmbedding(
                    embedding=self.embeddings[embedding_idx],
                    chunk=self.chunks[embedding_idx]
                )
            )
        
    def search(self, query, k):
        # embed the query
        query_embedding = embed([query])[0]
        dist = []
        
        # Get the euclidean distance of the query vector to all the cluster centers
        for cluster in self.cluster_centers:
            dist.append(euclidean_distance(query_embedding, cluster))
        
        # Find the cluster center with the smallest distance to the query vector
        cluster_idx = dist.index(min(dist))
        
        search_space = self.index[cluster_idx]
        
        # Perform a knn search over the embeddings in the cluster
        knn_engine = KNearNeighbors().fit([embedding.embedding for embedding in search_space])
        neighbors = knn_engine.predict(query_embedding, k)
        
        return [search_space[neighbor].chunk for neighbor in neighbors]

        
        
        
    