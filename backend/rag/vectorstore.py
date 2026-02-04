# Store & Retrieve Embeddings

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

_embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

_vectorstore = None


def add_documents(chunks):
    global _vectorstore

    if _vectorstore is None:
        _vectorstore = FAISS.from_documents(chunks, _embeddings)
    else:
        _vectorstore.add_documents(chunks)

def get_retriever(k: int = 4):
    if _vectorstore is None:
        raise RuntimeError("No documents uploaded yet")
    return _vectorstore.as_retriever(search_kwargs={"k": k})
