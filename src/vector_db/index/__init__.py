from .base import BaseIndex, BaseVectorSearchIndex
from .flatl2 import FlatL2Index
from .collections_index import CollectionsIndex
from .types import IndexTypes

class SearchIndex:
    
    def initialize_index(self, index_type: IndexTypes) -> BaseIndex:
        if index_type == IndexTypes.FLATL2:
            return FlatL2Index()
        elif index_type == IndexTypes.COLLECTIONS_INDEX:
            return CollectionsIndex()
        else:
            raise Exception(f'Index type {index_type} not supported')