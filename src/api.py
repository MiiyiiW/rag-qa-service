from fastapi import FastAPI

app = FastAPI(title="RAG QA Service")

@app.get("/")
def read_root():
    return {"service": "rag-qa-service", "status": "ok"}
