from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="News Content AI Service")

@app.get("/health")
def health():
    return {"status": "AI service running"}

app.include_router(router)
