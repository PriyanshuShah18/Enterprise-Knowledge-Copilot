# Question answering API

from fastapi import APIRouter
from backend.rag.chain import get_rag_chain
from backend.rag.vectorstore import get_retriever

router = APIRouter()

@router.post("/chat")
async def chat(query: str):
    retriever=get_retriever()
    docs= retriever.invoke(query)

    rag_chain = get_rag_chain()
    result = rag_chain.invoke(query)

    sources=list(
        {doc.metadata.get("source","unknown") for doc in docs}
    )

    return {
        "answer": result,
        "sources":sources

    }
