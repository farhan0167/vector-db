from typing import List, Dict
from .document import Document
from .chunk import Chunk
from .metadata import LibraryMetadata

from utils.index import recompute_index

class Library:
    def __init__(
        self, 
        name: str,
        metadata: LibraryMetadata
    ):
        self.name = name
        self.metadata = metadata
        self.documents: List[Document] = []
        self.__doc_name_index: Dict[str, int] = {}
        self.__doc_id_index: Dict[str, int] = {}
        
    def add_chunks(self, chunks: List[Chunk]):
        for chunk in chunks:
            chunk_meta = chunk.metadata
            doc = self.get_document(id=chunk_meta.doc_id)
            if not doc:
                continue
            doc.add_chunks([chunk])
    
    def get_chunk(self, chunk_id: str):
        pass
    
    def update_chunk(self):
        pass
    
    def remove_chunk(self):
        pass
    
    def add_document(self, document: Document) -> Document:
        # Check if the doc already exists
        if document.name in self.__doc_name_index:
            return None
        self.documents.append(document)
        self.__doc_name_index[document.name] = len(self.documents)-1
        self.__doc_id_index[document.id] = len(self.documents)-1
        
        return document
        
    def get_document(
        self, 
        name: str = None,
        id: str = None
    ) -> Document:
        if id and name:
            raise ValueError('Only one of `name` or `id` can be provided at a time.')
        if id:
            if not id in self.__doc_id_index:
                return None
            return self.documents[self.__doc_id_index[id]]
        if name:
            if not name in self.__doc_name_index:
                return None
        return self.documents[self.__doc_name_index[name]]
        
    def remove_document(self, name: str):
        if not name in self.__doc_name_index:
            return

        del self.__doc_id_index[ self.documents[ self.__doc_name_index[name] ].id ]
        del self.documents[self.__doc_name_index[name]]
        del self.__doc_name_index[name]
        
        # Recompute library name index
        self.__doc_name_index = recompute_index(
            iterable=self.documents,
            key='name'
        )
        self.__doc_id_index = recompute_index(
            iterable=self.documents,
            key='id'
        )

    def dict(self):
        return {
            'name': self.name
        }
    
    def json(self):
        pass
    