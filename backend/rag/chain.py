from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import re

from backend.config import GOOGLE_API_KEY,GROQ_API_KEY
from backend.rag.vectorstore import get_retriever


# -------- LLM (instantiate ONCE) --------
def get_llm():
    if GOOGLE_API_KEY:
        try:
            return ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.1,
                max_output_tokens=512,
                google_api_key=GOOGLE_API_KEY,
            )
        except Exception as e:
            print("Gemini init failed,Falling back to GROQ:",e)
    if GROQ_API_KEY:
        return ChatGroq(
            api_key=GROQ_API_KEY,
            model="qwen/qwen3-32b",
            max_tokens=512,
        )
    raise RuntimeError("No working LLM provider available")


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


def clean_llm_output(text:str)->str:
    # Remove <think>  from Groq response
    text=re.sub(r"<think>.*</think>","",text,flags=re.DOTALL)
    return text.strip()


_rag_chain = None



def get_rag_chain():
    global _rag_chain

    if _rag_chain is None:
        retriever = get_retriever()

        _rag_chain = (
            {
                "context": retriever,
                "question": RunnablePassthrough(),
            }
            | prompt
            | get_llm()                     # ✅ correct
            | StrOutputParser()
            | clean_llm_output
        )

    return _rag_chain
