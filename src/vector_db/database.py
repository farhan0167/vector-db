import threading
import time
from typing import List, Dict
from .library import Library
from exceptions import DuplicateError
from utils.index import recompute_index

class Database:
    def __init__(self):
        self.__lock = threading.Lock()
        self.libraries: List[Library] = []
        self.library_name_index: Dict[str, int] = {}
        
    def get_libraries(self) -> List[Library]:
        return [library for library in self.libraries]
    
    def get_library(
        self, 
        name: str
    ) -> Library:
        library_index = self.library_name_index.get(name)
        if library_index is None:
            raise KeyError(f'Library with name `{name}` does not exist.')
        return self.libraries[library_index]
    
    def add_library(
        self, 
        library: Library
    ) -> Library:
        
        if library.name in self.library_name_index:
            raise DuplicateError(f'Library with name `{library.name}` already exists. Please use a different name.')
        
        with self.__lock:
            self.libraries.append(library)
            self.library_name_index[library.name] = len(self.libraries)-1
        return library
    
    def update_library_name(
        self, 
        previous_name: str,
        new_name: str
    ) -> Library:
        if previous_name not in self.library_name_index:
            raise KeyError(f'Library with name `{previous_name}` does not exist.')
        if new_name in self.library_name_index:
            raise DuplicateError(f'Library with name `{new_name}` already exists. Please use a different name.')
        
        with self.__lock:
            # Get reference to the library
            library = self.libraries[self.library_name_index[previous_name]]
            # Update name
            library.name = new_name
            # Update library name index with new name
            self.library_name_index[new_name] = self.library_name_index[previous_name]
            # Remove previous name from index
            del self.library_name_index[previous_name]
            # Recompute library name index
            self.library_name_index = recompute_index(
                iterable=self.libraries,
                key='name'
            )
        return library
    
    def remove_library(
        self, 
        name: str
    ) -> None:
        
        if name not in self.library_name_index:
            raise KeyError(f'Library with name `{name}` does not exist.')
        
        with self.__lock:
            del self.libraries[self.library_name_index[name]]
            del self.library_name_index[name]
            
            # Recompute library name index
            self.library_name_index = recompute_index(
                iterable=self.libraries,
                key='name'
            )