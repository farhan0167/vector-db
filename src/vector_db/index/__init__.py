from .flatl2 import FlatL2Index
from .types import IndexTypes

class VectorSearchIndex:
    
    def initialize_index(self, index_type: IndexTypes):
        if index_type == IndexTypes.FLATL2:
            return FlatL2Index()
        else:
            raise Exception(f'Index type {index_type} not supported')