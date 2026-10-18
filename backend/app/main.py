from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import analysis

app = FastAPI(title="AI Resume Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5176",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5176",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router)


@app.get("/")
def root():
    return {"status": "AI Resume Analyzer API running"}
