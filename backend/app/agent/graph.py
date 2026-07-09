import json
import re
from datetime import date
from typing import Any, Dict, Literal

from langgraph.graph import END, START, StateGraph
from sqlalchemy.orm import Session

from app.agent.prompts import INTENT_EXTRACTION_SYSTEM_PROMPT, RESPONSE_SYSTEM_PROMPT
from app.agent.state import HCPAgentState
from app.agent.tools import (
    create_follow_up_task_tool,
    edit_interaction_tool,
    general_help_tool,
    get_hcp_profile_tool,
    log_interaction_tool,
    summarize_interaction_tool,
    suggest_next_action_tool,
)
from app.models import HCP
from app.services.groq_client import get_groq_service


VALID_TOOLS = {
    "log_interaction",
    "edit_interaction",
    "get_hcp_profile",
    "suggest_next_action",
    "create_follow_up_task",
    "summarize_interaction",
    "general_help",
}


def _extract_json(text: str) -> Dict[str, Any]:
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        return {
            "intent": "general_help",
            "tool_name": "general_help",
            "confidence": 0.0,
            "save_requested": False,
            "fields": {},
            "follow_up_task": {},
            "target_interaction_id": None,
            "missing_fields": ["Could not parse LLM JSON response"]
        }

    try:
        return json.loads(match.group(0))
    except Exception:
        return {
            "intent": "general_help",
            "tool_name": "general_help",
            "confidence": 0.0,
            "save_requested": False,
            "fields": {},
            "follow_up_task": {},
            "target_interaction_id": None,
            "missing_fields": ["Invalid JSON returned by LLM"]
        }


def load_context_node(state: HCPAgentState) -> Dict[str, Any]:
    db: Session = state["db"]
    selected_hcp_id = state.get("selected_hcp_id")

    hcp_context = {}

    if selected_hcp_id:
        hcp = db.query(HCP).filter(HCP.id == selected_hcp_id).first()

        if hcp:
            hcp_context = {
                "id": hcp.id,
                "name": hcp.name,
                "specialty": hcp.specialty,
                "territory": hcp.territory,
                "segment": hcp.segment,
                "preferred_channel": hcp.preferred_channel,
                "organization": hcp.organization,
                "last_interaction_date": hcp.last_interaction_date
            }

    return {
        "hcp_context": hcp_context,
        "current_form": state.get("current_form") or {}
    }


def intent_extraction_node(state: HCPAgentState) -> Dict[str, Any]:
    groq = get_groq_service()

    user_message = state["user_message"]
    current_form = state.get("current_form") or {}
    hcp_context = state.get("hcp_context") or {}

    extraction_prompt = f"""
Current date: {date.today().isoformat()}

Selected HCP context:
{json.dumps(hcp_context, default=str)}

Current form draft:
{json.dumps(current_form, default=str)}

User message:
{user_message}

Analyze the user message and return the JSON structure only.
"""

    raw_response = groq.chat_completion(
        messages=[
            {
                "role": "system",
                "content": INTENT_EXTRACTION_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": extraction_prompt
            }
        ],
        temperature=0.0,
        max_tokens=1000
    )

    extracted_data = _extract_json(raw_response)

    tool_name = extracted_data.get("tool_name") or extracted_data.get("intent") or "general_help"

    if tool_name not in VALID_TOOLS:
        tool_name = "general_help"

    return {
        "intent": extracted_data.get("intent", tool_name),
        "tool_name": tool_name,
        "confidence": float(extracted_data.get("confidence", 0.0) or 0.0),
        "extracted_data": extracted_data,
        "missing_fields": extracted_data.get("missing_fields", [])
    }


def route_tool(
    state: HCPAgentState
) -> Literal[
    "log_interaction",
    "edit_interaction",
    "get_hcp_profile",
    "suggest_next_action",
    "create_follow_up_task",
    "summarize_interaction",
    "general_help"
]:
    tool_name = state.get("tool_name", "general_help")

    if tool_name in VALID_TOOLS:
        return tool_name

    return "general_help"


def log_interaction_node(state: HCPAgentState) -> Dict[str, Any]:
    result = log_interaction_tool(
        db=state["db"],
        current_form=state.get("current_form") or {},
        extracted_data=state.get("extracted_data") or {},
        selected_hcp_id=state.get("selected_hcp_id")
    )

    return {
        "tool_result": result,
        "updated_form": result.get("updated_form", state.get("current_form") or {})
    }


def edit_interaction_node(state: HCPAgentState) -> Dict[str, Any]:
    result = edit_interaction_tool(
        db=state["db"],
        current_form=state.get("current_form") or {},
        extracted_data=state.get("extracted_data") or {}
    )

    return {
        "tool_result": result,
        "updated_form": result.get("updated_form", state.get("current_form") or {})
    }


def get_hcp_profile_node(state: HCPAgentState) -> Dict[str, Any]:
    result = get_hcp_profile_tool(
        db=state["db"],
        selected_hcp_id=state.get("selected_hcp_id"),
        extracted_data=state.get("extracted_data") or {}
    )

    updated_form = {
        **(state.get("current_form") or {}),
        **(result.get("updated_form") or {})
    }

    return {
        "tool_result": result,
        "updated_form": updated_form
    }


def suggest_next_action_node(state: HCPAgentState) -> Dict[str, Any]:
    result = suggest_next_action_tool(
        db=state["db"],
        current_form=state.get("current_form") or {},
        selected_hcp_id=state.get("selected_hcp_id"),
        extracted_data=state.get("extracted_data") or {}
    )

    return {
        "tool_result": result,
        "updated_form": result.get("updated_form", state.get("current_form") or {})
    }


def create_follow_up_task_node(state: HCPAgentState) -> Dict[str, Any]:
    result = create_follow_up_task_tool(
        db=state["db"],
        current_form=state.get("current_form") or {},
        extracted_data=state.get("extracted_data") or {},
        selected_hcp_id=state.get("selected_hcp_id")
    )

    return {
        "tool_result": result,
        "updated_form": result.get("updated_form", state.get("current_form") or {})
    }


def summarize_interaction_node(state: HCPAgentState) -> Dict[str, Any]:
    result = summarize_interaction_tool(
        db=state["db"],
        current_form=state.get("current_form") or {},
        extracted_data=state.get("extracted_data") or {}
    )

    return {
        "tool_result": result,
        "updated_form": result.get("updated_form", state.get("current_form") or {})
    }


def general_help_node(state: HCPAgentState) -> Dict[str, Any]:
    result = general_help_tool(
        db=state["db"],
        extracted_data=state.get("extracted_data") or {}
    )

    return {
        "tool_result": result,
        "updated_form": state.get("current_form") or {}
    }


def response_generation_node(state: HCPAgentState) -> Dict[str, Any]:
    groq = get_groq_service()

    tool_result = state.get("tool_result") or {}
    updated_form = state.get("updated_form") or state.get("current_form") or {}

    response_prompt = f"""
User message:
{state.get("user_message")}

Tool used:
{tool_result.get("tool_name")}

Tool result:
{json.dumps(tool_result, default=str)}

Updated form:
{json.dumps(updated_form, default=str)}

Write a short assistant response.
"""

    assistant_response = groq.chat_completion(
        messages=[
            {
                "role": "system",
                "content": RESPONSE_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": response_prompt
            }
        ],
        temperature=0.2,
        max_tokens=300
    )

    return {
        "assistant_response": assistant_response
    }


def build_hcp_agent_graph():
    graph = StateGraph(HCPAgentState)

    graph.add_node("load_context", load_context_node)
    graph.add_node("intent_extraction", intent_extraction_node)

    graph.add_node("log_interaction", log_interaction_node)
    graph.add_node("edit_interaction", edit_interaction_node)
    graph.add_node("get_hcp_profile", get_hcp_profile_node)
    graph.add_node("suggest_next_action", suggest_next_action_node)
    graph.add_node("create_follow_up_task", create_follow_up_task_node)
    graph.add_node("summarize_interaction", summarize_interaction_node)
    graph.add_node("general_help", general_help_node)

    graph.add_node("response_generation", response_generation_node)

    graph.add_edge(START, "load_context")
    graph.add_edge("load_context", "intent_extraction")

    graph.add_conditional_edges(
        "intent_extraction",
        route_tool,
        {
            "log_interaction": "log_interaction",
            "edit_interaction": "edit_interaction",
            "get_hcp_profile": "get_hcp_profile",
            "suggest_next_action": "suggest_next_action",
            "create_follow_up_task": "create_follow_up_task",
            "summarize_interaction": "summarize_interaction",
            "general_help": "general_help"
        }
    )

    graph.add_edge("log_interaction", "response_generation")
    graph.add_edge("edit_interaction", "response_generation")
    graph.add_edge("get_hcp_profile", "response_generation")
    graph.add_edge("suggest_next_action", "response_generation")
    graph.add_edge("create_follow_up_task", "response_generation")
    graph.add_edge("summarize_interaction", "response_generation")
    graph.add_edge("general_help", "response_generation")

    graph.add_edge("response_generation", END)

    return graph.compile()


hcp_agent_graph = build_hcp_agent_graph()


def run_hcp_agent(
    user_message: str,
    selected_hcp_id: int | None,
    current_form: Dict[str, Any],
    db: Session
) -> Dict[str, Any]:
    initial_state = {
        "user_message": user_message,
        "selected_hcp_id": selected_hcp_id,
        "current_form": current_form or {},
        "db": db
    }

    final_state = hcp_agent_graph.invoke(initial_state)

    return {
        "assistant_response": final_state.get("assistant_response"),
        "tool_name": final_state.get("tool_name"),
        "intent": final_state.get("intent"),
        "confidence": final_state.get("confidence"),
        "extracted_data": final_state.get("extracted_data"),
        "tool_result": final_state.get("tool_result"),
        "updated_form": final_state.get("updated_form") or current_form or {},
        "missing_fields": final_state.get("missing_fields", [])
    }