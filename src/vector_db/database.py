import threading
import time
from typing import List, Dict
from .library import Library
from exceptions import DuplicateError
from .index import SearchIndex, IndexTypes, CollectionsIndex

class Database:
    """ 
    The database is a collection of libraries.
    """
    def __init__(self):
        self.__lock = threading.Lock()
        self.libraries: List[Library] = []
        self.library_name_index: CollectionsIndex = SearchIndex().initialize_index(
            index_type=IndexTypes.COLLECTIONS_INDEX
        )
        
    def get_libraries(self) -> List[Library]:
        return self.libraries
     
    def get_library(
        self, 
        name: str
    ) -> Library:
        library_index = self.library_name_index.search(query=name)
        if library_index is None:
            raise KeyError(f'Library with name `{name}` does not exist.')
        return self.libraries[library_index]
    
    def add_library(
        self, 
        library: Library
    ) -> Library:
        
        if library.name in self.library_name_index.index:
            raise DuplicateError(f'Library with name `{library.name}` already exists. Please use a different name.')
        
        with self.__lock:
            self.libraries.append(library)
            self.library_name_index.add(
                id=library.name, 
                value=len(self.libraries)-1
            )
        return library
    
    def update_library_name(
        self, 
        previous_name: str,
        new_name: str
    ) -> Library:
        if previous_name not in self.library_name_index.index:
            raise KeyError(f'Library with name `{previous_name}` does not exist.')
        if new_name in self.library_name_index.index:
            raise DuplicateError(f'Library with name `{new_name}` already exists. Please use a different name.')
        
        with self.__lock:
            # Get reference to the library
            library = self.libraries[self.library_name_index.search(previous_name)]
            # Update name
            library.name = new_name
            # Update library name index with new name
            self.library_name_index.index[new_name] = self.library_name_index.index[previous_name]
            # Remove previous name from index
            self.library_name_index.remove(
                id=previous_name,
                iterable=self.libraries,
                reindex_key='name'
            )
        return library
    
    def remove_library(
        self, 
        name: str
    ) -> None:
        
        if name not in self.library_name_index.index:
            raise KeyError(f'Library with name `{name}` does not exist.')
        
        with self.__lock:
            del self.libraries[self.library_name_index.search(name)]
            self.library_name_index.remove(
                id=name,
                iterable=self.libraries,
                reindex_key='name'
            )