import os

from fastapi import APIRouter, HTTPException

from app.schemas import GroqTestRequest, GroqTestResponse
from app.services.groq_client import get_groq_service

import json
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AgentToolLog

router = APIRouter(
    prefix="/api/ai",
    tags=["AI"]
)


@router.post("/groq-test", response_model=GroqTestResponse)
def groq_test(payload: GroqTestRequest):
    try:
        groq_service = get_groq_service()

        response = groq_service.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant for a life sciences CRM. "
                        "Respond briefly and professionally."
                    )
                },
                {
                    "role": "user",
                    "content": payload.message
                }
            ]
        )

        return GroqTestResponse(
            model=os.getenv("GROQ_MODEL", "gemma2-9b-it"),
            response=response
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Groq test failed: {str(error)}"
        )

@router.get("/tool-logs")
def get_tool_logs(db: Session = Depends(get_db)):
    logs = db.query(AgentToolLog).order_by(
        AgentToolLog.created_at.desc()
    ).limit(20).all()

    return [
        {
            "id": log.id,
            "tool_name": log.tool_name,
            "status": log.status,
            "input_payload": json.loads(log.input_payload) if log.input_payload else None,
            "output_payload": json.loads(log.output_payload) if log.output_payload else None,
            "created_at": log.created_at
        }
        for log in logs
    ]