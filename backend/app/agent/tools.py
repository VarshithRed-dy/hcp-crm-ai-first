import json
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.models import AgentToolLog, FollowUpTask, HCP, Interaction
from app.services.groq_client import get_groq_service


FORM_FIELDS = [
    "hcp_id",
    "hcp_name",
    "interaction_type",
    "interaction_date",
    "interaction_time",
    "attendees",
    "topics_discussed",
    "materials_shared",
    "samples_distributed",
    "sentiment",
    "outcome",
    "next_step",
    "follow_up_date",
    "raw_notes",
    "ai_summary",
]


def _to_text(value: Any) -> Optional[str]:
    if value is None:
        return None

    if isinstance(value, list):
        return ", ".join(str(item) for item in value if item)

    if isinstance(value, dict):
        return json.dumps(value)

    return str(value)


def _clean_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    cleaned = {}

    for key, value in fields.items():
        if key not in FORM_FIELDS:
            continue

        if value is None:
            continue

        if isinstance(value, str) and value.strip() == "":
            continue

        if isinstance(value, list) and len(value) == 0:
            continue

        cleaned[key] = _to_text(value)

    return cleaned


def _find_hcp_by_name(db: Session, hcp_name: Optional[str]) -> Optional[HCP]:
    if not hcp_name:
        return None

    return db.query(HCP).filter(HCP.name.ilike(f"%{hcp_name}%")).first()


def _get_hcp(db: Session, hcp_id: Optional[int], hcp_name: Optional[str] = None) -> Optional[HCP]:
    if hcp_id:
        hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
        if hcp:
            return hcp

    return _find_hcp_by_name(db, hcp_name)


def log_tool_execution(
    db: Session,
    tool_name: str,
    input_payload: Dict[str, Any],
    output_payload: Dict[str, Any],
    status: str = "success"
) -> None:
    log = AgentToolLog(
        tool_name=tool_name,
        input_payload=json.dumps(input_payload, default=str),
        output_payload=json.dumps(output_payload, default=str),
        status=status
    )

    db.add(log)
    db.commit()


def log_interaction_tool(
    db: Session,
    current_form: Dict[str, Any],
    extracted_data: Dict[str, Any],
    selected_hcp_id: Optional[int]
) -> Dict[str, Any]:
    fields = _clean_fields(extracted_data.get("fields", {}))
    save_requested = bool(extracted_data.get("save_requested", False))

    updated_form = {
        **(current_form or {}),
        **fields
    }

    hcp = _get_hcp(
        db=db,
        hcp_id=selected_hcp_id or updated_form.get("hcp_id"),
        hcp_name=updated_form.get("hcp_name")
    )

    if hcp:
        updated_form["hcp_id"] = hcp.id
        updated_form["hcp_name"] = hcp.name

    saved_interaction_id = None

    if save_requested:
        interaction_data = {
            field: updated_form.get(field)
            for field in FORM_FIELDS
            if field != "id"
        }

        interaction = Interaction(**interaction_data)
        db.add(interaction)
        db.commit()
        db.refresh(interaction)

        saved_interaction_id = interaction.id
        updated_form["id"] = interaction.id

    result = {
        "tool_name": "log_interaction",
        "status": "success",
        "message": (
            "Interaction was saved successfully."
            if save_requested
            else "Interaction details were captured and the form was updated."
        ),
        "updated_form": updated_form,
        "saved_interaction_id": saved_interaction_id,
        "save_requested": save_requested
    }

    log_tool_execution(
        db=db,
        tool_name="log_interaction",
        input_payload=extracted_data,
        output_payload=result
    )

    return result


def edit_interaction_tool(
    db: Session,
    current_form: Dict[str, Any],
    extracted_data: Dict[str, Any]
) -> Dict[str, Any]:
    fields = _clean_fields(extracted_data.get("fields", {}))

    updated_form = {
        **(current_form or {}),
        **fields
    }

    target_interaction_id = (
        extracted_data.get("target_interaction_id")
        or updated_form.get("id")
    )

    db_updated = False

    if target_interaction_id:
        interaction = db.query(Interaction).filter(
            Interaction.id == int(target_interaction_id)
        ).first()

        if interaction:
            for key, value in fields.items():
                if hasattr(interaction, key):
                    setattr(interaction, key, value)

            db.commit()
            db.refresh(interaction)
            db_updated = True

    result = {
        "tool_name": "edit_interaction",
        "status": "success",
        "message": (
            "Interaction record and form were updated."
            if db_updated
            else "Form draft was updated."
        ),
        "updated_form": updated_form,
        "db_updated": db_updated
    }

    log_tool_execution(
        db=db,
        tool_name="edit_interaction",
        input_payload=extracted_data,
        output_payload=result
    )

    return result


def get_hcp_profile_tool(
    db: Session,
    selected_hcp_id: Optional[int],
    extracted_data: Dict[str, Any]
) -> Dict[str, Any]:
    fields = extracted_data.get("fields", {})
    hcp_name = fields.get("hcp_name")

    hcp = _get_hcp(
        db=db,
        hcp_id=selected_hcp_id or fields.get("hcp_id"),
        hcp_name=hcp_name
    )

    if not hcp:
        result = {
            "tool_name": "get_hcp_profile",
            "status": "not_found",
            "message": "HCP profile was not found.",
            "hcp_profile": None
        }

        log_tool_execution(db, "get_hcp_profile", extracted_data, result, "not_found")
        return result

    recent_interactions = db.query(Interaction).filter(
        Interaction.hcp_id == hcp.id
    ).order_by(Interaction.created_at.desc()).limit(3).all()

    profile = {
        "id": hcp.id,
        "name": hcp.name,
        "specialty": hcp.specialty,
        "territory": hcp.territory,
        "segment": hcp.segment,
        "preferred_channel": hcp.preferred_channel,
        "organization": hcp.organization,
        "last_interaction_date": hcp.last_interaction_date,
        "recent_interaction_count": len(recent_interactions)
    }

    result = {
        "tool_name": "get_hcp_profile",
        "status": "success",
        "message": f"HCP profile retrieved for {hcp.name}.",
        "hcp_profile": profile,
        "updated_form": {
            "hcp_id": hcp.id,
            "hcp_name": hcp.name
        }
    }

    log_tool_execution(db, "get_hcp_profile", extracted_data, result)
    return result


def suggest_next_action_tool(
    db: Session,
    current_form: Dict[str, Any],
    selected_hcp_id: Optional[int],
    extracted_data: Dict[str, Any]
) -> Dict[str, Any]:
    hcp_id = selected_hcp_id or current_form.get("hcp_id")

    hcp = _get_hcp(
        db=db,
        hcp_id=hcp_id,
        hcp_name=current_form.get("hcp_name")
    )

    recent_interactions = []

    if hcp:
        recent_interactions = db.query(Interaction).filter(
            Interaction.hcp_id == hcp.id
        ).order_by(Interaction.created_at.desc()).limit(5).all()

    history_text = "\n".join(
        [
            f"- {item.interaction_date}: {item.ai_summary or item.topics_discussed or item.raw_notes}"
            for item in recent_interactions
        ]
    )

    groq = get_groq_service()

    prompt = f"""
Suggest the next best action for a life sciences sales representative.

HCP:
{hcp.name if hcp else current_form.get("hcp_name", "Unknown")}

Current form:
{json.dumps(current_form, default=str)}

Recent interaction history:
{history_text if history_text else "No prior history available."}

Return a short recommendation with:
1. Recommended next action
2. Reason
3. Suggested follow-up timing
"""

    recommendation = groq.chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a CRM sales assistant for life sciences field representatives."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=400
    )

    updated_form = {
        **(current_form or {}),
        "next_step": recommendation
    }

    result = {
        "tool_name": "suggest_next_action",
        "status": "success",
        "message": "Next best action recommendation generated.",
        "recommendation": recommendation,
        "updated_form": updated_form
    }

    log_tool_execution(db, "suggest_next_action", extracted_data, result)
    return result


def create_follow_up_task_tool(
    db: Session,
    current_form: Dict[str, Any],
    extracted_data: Dict[str, Any],
    selected_hcp_id: Optional[int]
) -> Dict[str, Any]:
    task_data = extracted_data.get("follow_up_task", {}) or {}

    task_title = task_data.get("task_title") or current_form.get("next_step") or "Follow up with HCP"
    task_description = task_data.get("task_description") or current_form.get("next_step")
    due_date = task_data.get("due_date") or current_form.get("follow_up_date")

    hcp_id = selected_hcp_id or current_form.get("hcp_id")
    interaction_id = current_form.get("id")

    task = FollowUpTask(
        interaction_id=interaction_id,
        hcp_id=hcp_id,
        task_title=task_title,
        task_description=task_description,
        due_date=due_date,
        status="Open"
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    result = {
        "tool_name": "create_follow_up_task",
        "status": "success",
        "message": "Follow-up task created successfully.",
        "task": {
            "id": task.id,
            "interaction_id": task.interaction_id,
            "hcp_id": task.hcp_id,
            "task_title": task.task_title,
            "task_description": task.task_description,
            "due_date": task.due_date,
            "status": task.status
        },
        "updated_form": current_form
    }

    log_tool_execution(db, "create_follow_up_task", extracted_data, result)
    return result


def summarize_interaction_tool(
    db: Session,
    current_form: Dict[str, Any],
    extracted_data: Dict[str, Any]
) -> Dict[str, Any]:
    fields = extracted_data.get("fields", {})
    raw_notes = (
        fields.get("raw_notes")
        or current_form.get("raw_notes")
        or current_form.get("topics_discussed")
        or ""
    )

    groq = get_groq_service()

    summary = groq.chat_completion(
        messages=[
            {
                "role": "system",
                "content": (
                    "You summarize life sciences HCP interaction notes into concise, "
                    "CRM-safe language. Do not add unsupported claims."
                )
            },
            {
                "role": "user",
                "content": f"Summarize these interaction notes for CRM:\n\n{raw_notes}"
            }
        ],
        temperature=0.2,
        max_tokens=300
    )

    updated_form = {
        **(current_form or {}),
        "raw_notes": raw_notes,
        "ai_summary": summary
    }

    result = {
        "tool_name": "summarize_interaction",
        "status": "success",
        "message": "Interaction summary generated.",
        "summary": summary,
        "updated_form": updated_form
    }

    log_tool_execution(db, "summarize_interaction", extracted_data, result)
    return result


def general_help_tool(
    db: Session,
    extracted_data: Dict[str, Any]
) -> Dict[str, Any]:
    result = {
        "tool_name": "general_help",
        "status": "success",
        "message": (
            "You can ask me to log an HCP interaction, edit a field, retrieve an HCP profile, "
            "suggest a next action, create a follow-up task, or summarize notes."
        ),
        "updated_form": {}
    }

    log_tool_execution(db, "general_help", extracted_data, result)
    return result