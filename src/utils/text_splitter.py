from typing import List

class TextSplitter:
    def __init__(
        self, 
        chunk_size: int
    ):
        self.chunk_size = chunk_size
        
    def split_text(self, text: str) -> List[str]:
        per_chunk = len(text) // self.chunk_size
        chunks = [text[i:i+per_chunk] for i in range(0, len(text), per_chunk)]
        return chunks
    
    