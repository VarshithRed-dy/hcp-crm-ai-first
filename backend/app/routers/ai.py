import os

from fastapi import APIRouter, HTTPException

from app.schemas import GroqTestRequest, GroqTestResponse
from app.services.groq_client import get_groq_service

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