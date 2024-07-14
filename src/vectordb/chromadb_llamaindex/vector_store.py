# vector_store.py located in src/vectordb/chromadb_llamaindex

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

class VectorStore:
    def __init__(self, vector_store, storage_dir, input_dir):
        self.vector_store = vector_store
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.storage_dir = storage_dir
        self.input_dir = input_dir  # Directory where documents are stored

    def read_documents(self):
        """ Reads documents from the input directory using SimpleDirectoryReader. """
        reader = SimpleDirectoryReader(input_dir=self.input_dir)
        return reader.load_data()

    def create_index(self):
        """ Creates an index from documents read from the input directory. """
        documents = self.read_documents()
        index = VectorStoreIndex.from_documents(documents, storage_context=self.storage_context, show_progress=True)
        index.storage_context.persist(persist_dir=self.storage_dir)
        self.query_engine = index.as_query_engine()
        return index
    
    def load_index(self):
        """ Loads an index from the storage directory. """
        index = VectorStoreIndex.load_from_storage(self.storage_context)
        self.query_engine = index.as_query_engine()
        return index
    
    def query(self, query):
        """ Queries the given index with a specified query vector. """
        return self.query_engine.query(query)

def setup_chroma_vector_store(storage_path, collection_name, embedding):
    """
    Setup Chroma vector store with an embedding model.

    Args:
    storage_path (str): Path to the storage directory for ChromaDB.
    embedding (EmbeddingModel): The embedding model to use for vector operations.

    Returns:
    ChromaVectorStore: Configured Chroma vector store.
    """
    db = chromadb.PersistentClient(path=storage_path)
    chroma_collection = db.get_or_create_collection(collection_name)
    return ChromaVectorStore(chroma_collection=chroma_collection, embed_model=embedding)