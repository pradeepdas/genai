import os
from pathlib import Path
from src.vectordb.chromadb_llamaindex.vector_store import VectorStore, setup_chroma_vector_store
from llama_index.embeddings.openai import OpenAIEmbedding

def run_test():
    # Get the OpenAI API key from environment variables
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Define the storage path for ChromaDB and the directory containing the test documents
    storage_path = "db/chromadb-llamaindex/storage"
    input_directory = Path("tests/test_data")  # Adjusted path to match your correct data location
    
    # Setup the embedding model using the OpenAI API key
    embedding_model = OpenAIEmbedding(model='text-embedding-3-small', api_key=openai_api_key)

    # Setup the vector store using the Chroma configuration with the embedding model
    vector_store = setup_chroma_vector_store(str(storage_path), "test", embedding_model)

    # Initialize the VectorStore class with paths
    document_processor = VectorStore(vector_store, str(storage_path), str(input_directory))

    # Create the index from documents in the specified input directory
    index = document_processor.create_index()
    print("Index created and persisted successfully.")

    results = document_processor.query("diabetes guideline for albminuria")
    print("Query Results:", results, "\n")

    results = document_processor.query("provide a pea soup recipe")
    print("Query Results:", results, "\n")

if __name__ == '__main__':
    run_test()
