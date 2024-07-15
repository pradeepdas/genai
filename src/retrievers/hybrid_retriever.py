import os

from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.output_parsers import StrOutputParser

from src.chains.basic_chain import get_model
from src.chains.rag_chain import make_rag_chain
from src.loaders.remote.remote_loader import lc_load_web_page
from src.processing.splitter import split_documents
from src.vectordb.chromadb_langchain.vector_store import create_vector_db
from dotenv import load_dotenv


def ensemble_retriever_from_docs(docs, embeddings=None):
    texts = split_documents(docs)
    vs = create_vector_db(texts, embeddings)
    vs_retriever = vs.as_retriever()

    bm25_retriever = BM25Retriever.from_texts([t.page_content for t in texts])

    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vs_retriever],
        weights=[0.5, 0.5])

    return ensemble_retriever


def main():
    load_dotenv()

    problems_of_philosophy_by_russell = "https://www.gutenberg.org/ebooks/5827.html.images"
    docs = lc_load_web_page(problems_of_philosophy_by_russell)
    ensemble_retriever = ensemble_retriever_from_docs(docs)
    model = get_model("ChatGPT")
    chain = make_rag_chain(model, ensemble_retriever) | StrOutputParser()

    result = chain.invoke("What are the key problems of philosophy according to Russell?")
    print(result)


if __name__ == "__main__":
    # this is to quite parallel tokenizers warning.
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    main()