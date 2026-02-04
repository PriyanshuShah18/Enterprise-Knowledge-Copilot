from fastapi import FastAPI
from backend.api.upload import router as upload_router
from backend.api.chat import router as chat_router

app = FastAPI(title="Smart Document Assistant API")

app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/")
def health():
    return {"status": "API running"}
