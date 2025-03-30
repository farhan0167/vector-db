import math

class KNearNeighbors:
    """A simple implementation of the K nearest neighbors algorithm."""
    def __init__(self):
        self.X = []
        """X: List of embeddings or the vector space to search in."""
        
    def fit(self, X):
        """
        Fit the model with a set of embeddings.
        """
        self.X = X
        return self
        
    def compute_distance(self, query):
        """Compute the distance between the query and all the embeddings."""
        dist = []
        for embedding in self.X:
            pairwise_sum = 0
            for i in range(len(embedding)):
                pairwise_sum+= (embedding[i]-query[i])**2
            dist.append(math.sqrt(pairwise_sum))
        return dist
    
    def argsort(self, hist):
        """Simple implementation of argsort."""
        return sorted(range(len(hist)), key=lambda i: hist[i])
    
    def predict(self, query, k):
        """Predict the k nearest neighbors."""
        hist = self.compute_distance(query)
        return self.argsort(hist)[:k]
        