import uuid
from typing import Dict, Any

class Chunk:
    def __init__(
        self, 
        text: str,
        metadata: Dict[str, Any]
    ):
        self.id = str(uuid.uuid4())
        self.text = text
        self.embedding = None
        self.metadata = metadata
    
    def __repr__(self):
        return f"Chunk(id='{self.id}', text='{self.text[:20]}..', metadata={self.metadata})"
    
    def dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "embedding": self.embedding[: 5] if self.embedding else None,
            "metadata": self.metadata
        }