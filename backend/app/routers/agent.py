from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.agent.graph import run_hcp_agent
from app.database import get_db
from app.schemas import AgentChatRequest, AgentChatResponse

router = APIRouter(
    prefix="/api/agent",
    tags=["LangGraph Agent"]
)


@router.post("/chat", response_model=AgentChatResponse)
def agent_chat(
    payload: AgentChatRequest,
    db: Session = Depends(get_db)
):
    try:
        result = run_hcp_agent(
            user_message=payload.message,
            selected_hcp_id=payload.selected_hcp_id,
            current_form=payload.current_form or {},
            db=db
        )

        return AgentChatResponse(
            assistant_response=result.get("assistant_response") or "Done.",
            tool_name=result.get("tool_name"),
            intent=result.get("intent"),
            confidence=result.get("confidence"),
            extracted_data=result.get("extracted_data"),
            tool_result=result.get("tool_result"),
            updated_form=result.get("updated_form") or {},
            missing_fields=result.get("missing_fields") or []
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(error)}"
        )