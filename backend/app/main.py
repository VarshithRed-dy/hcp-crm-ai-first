from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import HCP

app = FastAPI(
    title="AI-First CRM HCP Module",
    description="FastAPI backend for AI-first HCP interaction logging",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "AI-First CRM HCP backend is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/api/hcps")
def get_hcps():
    return [
        {
            "id": 1,
            "name": "Dr. Smith",
            "specialty": "Cardiology",
            "territory": "Dallas",
            "segment": "High Value",
            "preferred_channel": "In-person"
        },
        {
            "id": 2,
            "name": "Dr. Rao",
            "specialty": "Endocrinology",
            "territory": "Plano",
            "segment": "Medium Value",
            "preferred_channel": "Email"
        }
    ]