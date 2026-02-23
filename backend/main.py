"""
Aura / VibeSync — FastAPI Backend
NLP Mental Health Triage Ecosystem
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from routes.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🧠 Aura NLP Engine starting...")
    yield
    print("🛑 Aura shutting down.")


app = FastAPI(
    title="Aura — Mental Health Triage API",
    description="NLP-powered mental health triage backend. NOT a medical device.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow Quasar dev server and production PWA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api")


@app.get("/")
async def root():
    return {"status": "ok", "service": "Aura NLP Engine v1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
