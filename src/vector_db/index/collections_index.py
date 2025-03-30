from typing import Dict, List, Union
from .base import BaseIndex

class CollectionsIndex(BaseIndex):
    """ 
    In vector-db, we store a lot of data in collections, or in python terms, in a List.
    For example, a library is a collection(list) of documents, and a document is a collection(list) of chunks.
    
    Searching for an object within a list, in the most simplest case, is a linear search which has a time complexity 
    of O(n). We can improve that by keeping a CollectionsIndex, which basically indexes an object by its name to its index
    in the list.
    
    ## Building the index:
    The index is built everytime a tracked object adds some child object to it via some list append operation. This is
    an O(1) operation.
    
    ## Searching:
    The search operation is also an O(1) operation since the accessing a hashmap is an O(1) operation.
    
    ## Removing:
    The remove operation however would mean that we need to recompute the index once an object is evited from the list.
    This is an O(n) operation. But we are okay with this since the main objective of the retrieval system is to provide
    fast retrieval/search for the user.
    
    Index: dict of {
        key(some identifier, id): value(index in the list)
    }
    """
    def __init__(self):
        self.index: Dict[str, int] = {}
        
    def search(
        self,
        query: str
    ) -> int:
        """Searching for an object's index is an O(1) operation since we have a hash map."""
        return self.index.get(query)
    
    def add(self, id: str, value: int):
        self.index[id] = value
    
    def remove(self, id: str, iterable: List, reindex_key: str):
        del self.index[id]
        # Recompute index
        self.index = self.build_index(
            iterable=iterable,
            key=reindex_key
        )
    
    def build_index(
        self,
        iterable: List,
        key: str
    ):
        return {
            getattr(item, key): i
            for i, item in enumerate(iterable)
        }