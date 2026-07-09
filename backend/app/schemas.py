from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class HCPBase(BaseModel):
    name: str
    specialty: Optional[str] = None
    territory: Optional[str] = None
    segment: Optional[str] = None
    preferred_channel: Optional[str] = None
    organization: Optional[str] = None
    last_interaction_date: Optional[str] = None


class HCPCreate(HCPBase):
    pass


class HCPResponse(HCPBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class InteractionBase(BaseModel):
    hcp_id: Optional[int] = None
    hcp_name: Optional[str] = None

    interaction_type: Optional[str] = None
    interaction_date: Optional[str] = None
    interaction_time: Optional[str] = None

    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None

    sentiment: Optional[str] = None
    outcome: Optional[str] = None
    next_step: Optional[str] = None
    follow_up_date: Optional[str] = None

    raw_notes: Optional[str] = None
    ai_summary: Optional[str] = None
    source: Optional[str] = "AI Assistant"


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    hcp_id: Optional[int] = None
    hcp_name: Optional[str] = None

    interaction_type: Optional[str] = None
    interaction_date: Optional[str] = None
    interaction_time: Optional[str] = None

    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None

    sentiment: Optional[str] = None
    outcome: Optional[str] = None
    next_step: Optional[str] = None
    follow_up_date: Optional[str] = None

    raw_notes: Optional[str] = None
    ai_summary: Optional[str] = None
    source: Optional[str] = None


class InteractionResponse(InteractionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FollowUpTaskCreate(BaseModel):
    interaction_id: Optional[int] = None
    hcp_id: Optional[int] = None
    task_title: str
    task_description: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = "Open"


class FollowUpTaskResponse(FollowUpTaskCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GroqTestRequest(BaseModel):
    message: str


class GroqTestResponse(BaseModel):
    model: str
    response: str

class AgentChatRequest(BaseModel):
    message: str
    selected_hcp_id: Optional[int] = None
    current_form: Optional[Dict[str, Any]] = {}


class AgentChatResponse(BaseModel):
    assistant_response: str
    tool_name: Optional[str] = None
    intent: Optional[str] = None
    confidence: Optional[float] = None
    extracted_data: Optional[Dict[str, Any]] = None
    tool_result: Optional[Dict[str, Any]] = None
    updated_form: Dict[str, Any] = {}
    missing_fields: List[str] = []