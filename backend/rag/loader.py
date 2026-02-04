# Load Documents

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)

def load_document(path: str):
    if path.endswith(".pdf"):
        loader = PyPDFLoader(path)
    elif path.endswith(".txt"):
        loader = TextLoader(path)
    elif path.endswith(".docx"):
        loader = Docx2txtLoader(path)
    else:
        raise ValueError("Unsupported file type")

    docs = loader.load()

    # Add filename metadata
    for doc in docs:
        doc.metadata["source"] = path.split("/")[-1]

    return docs
