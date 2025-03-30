

class KNearNeighbors:
    def __init__(self):
        self.X = []
        
    def fit(self, X):
        self.X = X
        return self
        
    def compute_distance(self, query):
        dist = []
        for embedding in self.X:
            pairwise_sum = 0
            for i in range(len(embedding)):
                pairwise_sum+= (embedding[i]-query[i])**2
            dist.append(pairwise_sum)
        return dist
    
    def argsort(self, hist):
        return sorted(range(len(hist)), key=lambda i: hist[i])
    
    def predict(self, query, k):
        hist = self.compute_distance(query)
        return self.argsort(hist)[:k]
        