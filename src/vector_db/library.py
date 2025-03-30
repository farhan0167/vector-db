from typing import List, Dict, Any, Union
from .document import Document
from .chunk import Chunk
from .index import SearchIndex, IndexTypes, BaseIndex, BaseVectorSearchIndex
from utils.index import recompute_index
from exceptions import DuplicateError

class Library:
    def __init__(
        self, 
        name: str,
        metadata: Dict[str, Any]
    ):
        self.name = name
        self.metadata = metadata
        self.documents: List[Document] = []
        self.index: Union[BaseVectorSearchIndex, None] = None
        # Document relted index
        self.__doc_name_index: Dict[str, int] = {}
        self.__doc_id_index: Dict[str, int] = {}
        # Chunk related index
        self.__chunk_id_to_doc_id: Dict[str, str] = {}
        
    def add_vector_search_index(self, index_type: IndexTypes):
        self.index = SearchIndex().initialize_index(
            index_type=index_type
        )
        
    def build_index(self):
        self.index.build_index()
        
    def search(self, query, k):
        return self.index.search(query=query, k=k)
        
    def add_chunks(self, chunks: List[Chunk]):
        chunks_added = []
        for chunk in chunks:
            chunk_meta = chunk.metadata
            doc_id = chunk_meta.get('doc_id')
            try:
                doc = self.get_document(id=doc_id)
            except KeyError:
                for added_chunk in chunks_added:
                    self.remove_chunk(added_chunk.id)
                raise KeyError(f'Document with id `{doc_id}` does not exist.')
            try:
                doc.add_chunk(chunk)
            except DuplicateError as e:
                for added_chunk in chunks_added:
                    self.remove_chunk(added_chunk.id)
                raise DuplicateError(f'Chunk with id `{chunk.id}` already exists. Removing all previous chunks already added.')
            chunks_added.append(chunk)
            self.__chunk_id_to_doc_id[chunk.id] = doc.id
        self.index.add(chunks=chunks)
    
    def get_chunk(self, chunk_id: str) -> Chunk:
        doc_id = self.__chunk_id_to_doc_id.get(chunk_id)
        if not doc_id:
            raise KeyError(f'Chunk with id `{chunk_id}` not found. There is no document associated with this chunk.')
        doc = self.get_document(id=doc_id)
        return doc.get_chunk(chunk_id)
    
    def get_chunks(self) -> List[Chunk]:
        """Get all chunks from the library. If index is not built, 
        then go over every document to get the chunks. Time complexity: O(D),
        where D is the number of documents in the library.
        
        However, if the index is built, then time complexity: O(1).
        """
        if not self.index:
            chunks = []
            docs = self.get_documents()
            for doc in docs:
                chunks.extend(doc.get_chunks())
        return self.index.get_chunks()
    
    def update_chunk(
        self, 
        chunk_id: str, 
        text: str
    ) -> Chunk:
        doc_id = self.__chunk_id_to_doc_id.get(chunk_id)
        if not doc_id:
            raise KeyError(f'Chunk with id `{chunk_id}` not found. There is no document associated with this chunk.')
        doc = self.get_document(id=doc_id)
        doc._update_chunk_text(chunk_id=chunk_id, text=text)
        # TODO update vector search index
    
    def remove_chunk(self, chunk_id: str):
        # Get the document the chunk is associated with
        doc_id = self.__chunk_id_to_doc_id.get(chunk_id)
        if not doc_id:
            raise KeyError(f'Chunk with id `{chunk_id}` not found. There is no document associated with this chunk.')
        # Delete the chunk from the __chunk_id_to_doc
        del self.__chunk_id_to_doc_id[chunk_id]
        # Get the document
        doc = self.get_document(id=doc_id)
        # Remove the chunk from the document
        doc._remove_chunk(chunk_id)
        # TODO update vector search index
        
    def get_documents(self) -> List[Document]:
        return self.documents
    
    def add_document(self, document: Document) -> Document:
        # Check if the doc already exists
        if document.name in self.__doc_name_index:
            raise DuplicateError(f'Document with name `{document.name}` already exists.')
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
                raise KeyError(f'Document with id `{id}` does not exist.')
            return self.documents[self.__doc_id_index[id]]
        if name:
            if not name in self.__doc_name_index:
                raise KeyError(f'Document with name `{name}` does not exist.')
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
            'name': self.name,
            'metadata': self.metadata
        }
    
    def json(self):
        pass
    