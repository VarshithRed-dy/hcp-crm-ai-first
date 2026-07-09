from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class HCPAgentState(TypedDict, total=False):
    user_message: str
    selected_hcp_id: Optional[int]
    current_form: Dict[str, Any]

    hcp_context: Dict[str, Any]

    intent: str
    tool_name: str
    confidence: float
    extracted_data: Dict[str, Any]
    missing_fields: List[str]

    tool_result: Dict[str, Any]
    updated_form: Dict[str, Any]
    assistant_response: str

    db: Any