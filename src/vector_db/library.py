from typing import List, Dict, Any, Union
from .document import Document
from .chunk import Chunk
from .index import (
    SearchIndex, 
    IndexTypes, 
    BaseIndex, 
    BaseVectorSearchIndex,
    CollectionsIndex
)
from exceptions import DuplicateError

class Library:
    """ 
    A library is a collection of documents. The library acts as a controller/interface
    for both the documents and its chunks. Any interaction on documents and chunks are 
    handled by the library even though documents are the one's managing their chunks.
    
    The library stores 3 indexes. There are two indexes of type `COLLECTIONS_INDEX` that
    index the documents by its name and id. The other index is of type `VECTOR_SEARCH_INDEX`
    that indexes the chunks, which is used by the vector search index to do RAG stuff.
    
    One thing to note about Documents within a library is that it's name is unique.
    """
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
        self.__doc_name_index: CollectionsIndex = SearchIndex().initialize_index(
            index_type=IndexTypes.COLLECTIONS_INDEX
        )
        self.__doc_id_index: CollectionsIndex = SearchIndex().initialize_index(
            index_type=IndexTypes.COLLECTIONS_INDEX
        )
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
        """Get a chunk from the library. This is an O(1) operation since
        we have indexed both a chunk_id to doc_id mapping, and a doc_id to its
        index in the document list. From there, getting the chunk is also an O(1)
        operation since inside the document, we have a list of chunks indexed
        by its id.
        """
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
        """Update the text of a chunk and update the vector search index."""
        doc_id = self.__chunk_id_to_doc_id.get(chunk_id)
        if not doc_id:
            raise KeyError(f'Chunk with id `{chunk_id}` not found. There is no document associated with this chunk.')
        doc = self.get_document(id=doc_id)
        doc._update_chunk_text(chunk_id=chunk_id, text=text)
        # TODO update vector search index
        
    
    def remove_chunk(self, chunk_id: str):
        """Remove a chunk from the library."""
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
        """ Add a document to the library. If the document already exists, then raise an error."""
        # Check if the doc already exists
        if document.name in self.__doc_name_index.index:
            raise DuplicateError(f'Document with name `{document.name}` already exists.')
        self.documents.append(document)
        self.__doc_name_index.add(id=document.name, value=len(self.documents)-1)
        self.__doc_id_index.add(id=document.id, value=len(self.documents)-1)
        
        # If chunks were already added
        if document.chunks:
            self.add_chunks(document.chunks)
        
        return document
        
    def get_document(
        self, 
        name: str = None,
        id: str = None
    ) -> Document:
        """ Get a document from the library. If both name and id are provided, then raise an error. """
        if id and name:
            raise ValueError('Only one of `name` or `id` can be provided at a time.')
        if id:
            if not id in self.__doc_id_index.index:
                raise KeyError(f'Document with id `{id}` does not exist.')
            return self.documents[self.__doc_id_index.search(id)]
        if name:
            if not name in self.__doc_name_index.index:
                raise KeyError(f'Document with name `{name}` does not exist.')
        return self.documents[self.__doc_name_index.search(name)]
        
    def remove_document(self, id: str):
        """ Remove a document from the library. """
        if not id in self.__doc_id_index.index:
            raise KeyError(f'Document with id `{id}` does not exist.')
        
        doc = self.get_document(id=id)
        for chunk in doc.get_chunks():
            self.remove_chunk(chunk_id=chunk.id)
        doc_index = self.__doc_id_index.search(id)
        del self.documents[doc_index]
        self.__doc_id_index.remove(
            id=doc.id,
            iterable=self.documents,
            reindex_key='id'
        )
        self.__doc_name_index.remove(
            id=doc.name,
            iterable=self.documents,
            reindex_key='name'
        )

    def dict(self):
        return {
            'name': self.name,
            'metadata': self.metadata
        }
    
    def json(self):
        pass
    