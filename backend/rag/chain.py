# API Entry Point

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from backend.config import GOOGLE_API_KEY
from backend.rag.vectorstore import get_retriever


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        max_output_tokens=512,
        )



'''ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    #max_output_tokens=512,
    google_api_key=GOOGLE_API_KEY,
)'''

prompt = ChatPromptTemplate.from_template(
"""
You are an enterprise document assistant.

Answer ONLY using the provided context.
If the answer is not present in the context, respond exactly with:
"Out of Context."

Context:
{context}

Question:
{question}

Answer:
"""
)

def get_rag_chain():
    retriever = get_retriever()

    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }
        | prompt
        | get_llm
        | StrOutputParser()
    )

    return rag_chain
