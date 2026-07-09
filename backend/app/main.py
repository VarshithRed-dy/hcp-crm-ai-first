from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, SessionLocal, engine
from app.routers import agent, ai, hcp, interactions
from app.seed_data import seed_hcps


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_hcps(db)
    finally:
        db.close()

    yield


app = FastAPI(
    title="AI-First CRM HCP Module",
    description="FastAPI backend for AI-first HCP interaction logging",
    version="0.2.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hcp.router)
app.include_router(interactions.router)
app.include_router(ai.router)
app.include_router(agent.router)


@app.get("/")
def root():
    return {
        "message": "AI-First CRM HCP backend is running",
        "version": "0.2.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }