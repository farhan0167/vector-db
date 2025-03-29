from typing import List, Dict
from .document import Document
from .chunk import Chunk
from .metadata import LibraryMetadata
from .index import VectorSearchIndex, IndexTypes
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
        self.index = None
        # Document relted index
        self.__doc_name_index: Dict[str, int] = {}
        self.__doc_id_index: Dict[str, int] = {}
        # Chunk related index
        self.__chunk_id_to_doc_id: Dict[str, str] = {}
        
    def add_vector_search_index(self, index_type: IndexTypes):
        self.index = VectorSearchIndex().initialize_index(
            index_type=index_type
        )
        
    def build_index(self):
        self.index.build_index()
        
    def search(self, query, k):
        return self.index.search(query=query, k=k)
        
    def add_chunks(self, chunks: List[Chunk]):
        for chunk in chunks:
            chunk_meta = chunk.metadata
            doc = self.get_document(id=chunk_meta.doc_id)
            if not doc:
                # TODO: If not doc then perhaps create one?
                continue
            doc.add_chunk(chunk)
            self.__chunk_id_to_doc_id[chunk.id] = doc.id
        self.index.add(chunks=chunks)
    
    def get_chunk(self, chunk_id: str) -> Chunk:
        doc_id = self.__chunk_id_to_doc_id[chunk_id]
        doc = self.get_document(id=doc_id)
        return doc.get_chunk(chunk_id)
    
    def update_chunk(
        self, 
        chunk_id: str, 
        text: str
    ) -> Chunk:
        doc_id = self.__chunk_id_to_doc_id[chunk_id]
        doc = self.get_document(id=doc_id)
        doc._update_chunk_text(chunk_id=chunk_id, text=text)
        # TODO update vector search index
    
    def remove_chunk(self, chunk_id: str):
        # Get the document the chunk is associated with
        doc_id = self.__chunk_id_to_doc_id[chunk_id]
        # Delete the chunk from the __chunk_id_to_doc
        del self.__chunk_id_to_doc_id[chunk_id]
        # Get the document
        doc = self.get_document(id=doc_id)
        # Remove the chunk from the document
        doc._remove_chunk(chunk_id)
        # TODO update vector search index
    
    def add_document(self, document: Document) -> Document:
        # Check if the doc already exists
        if document.name in self.__doc_name_index:
            return None
        self.documents.append(document)
        self.__doc_name_index[document.name] = len(self.documents)-1
        self.__doc_id_index[document.id] = len(self.documents)-1
        
        # If chunks were already added
        if document.chunks:
            self.add_chunks(document.chunks)
        
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
        
    def remove_document(self, id: str):
        if not id in self.__doc_id_index:
            return
        
        doc = self.get_document(id=id)
        for chunk in doc.get_chunks():
            self.remove_chunk(chunk_id=chunk.id)
        doc_index = self.__doc_id_index[id]
        del self.__doc_id_index[id]
        del self.__doc_name_index[doc.name]
        del self.documents[doc_index]
        
        
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
    