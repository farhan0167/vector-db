import threading
import time
from typing import List, Dict
from .library import Library
from exceptions import DuplicateError

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
            self.library_name_index = {
                library.name: i
                for i, library in enumerate(self.libraries)
            }