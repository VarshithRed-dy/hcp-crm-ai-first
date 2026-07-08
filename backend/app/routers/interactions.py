from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Interaction
from app.schemas import InteractionCreate, InteractionResponse, InteractionUpdate

router = APIRouter(
    prefix="/api/interactions",
    tags=["Interactions"]
)


@router.post("/", response_model=InteractionResponse)
def create_interaction(
    payload: InteractionCreate,
    db: Session = Depends(get_db)
):
    interaction = Interaction(**payload.model_dump())
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.get("/", response_model=List[InteractionResponse])
def get_interactions(
    hcp_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Interaction)

    if hcp_id is not None:
        query = query.filter(Interaction.hcp_id == hcp_id)

    return query.order_by(Interaction.created_at.desc()).all()


@router.get("/{interaction_id}", response_model=InteractionResponse)
def get_interaction_by_id(
    interaction_id: int,
    db: Session = Depends(get_db)
):
    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    return interaction


@router.put("/{interaction_id}", response_model=InteractionResponse)
def update_interaction(
    interaction_id: int,
    payload: InteractionUpdate,
    db: Session = Depends(get_db)
):
    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(interaction, field, value)

    db.commit()
    db.refresh(interaction)
    return interaction


@router.delete("/{interaction_id}")
def delete_interaction(
    interaction_id: int,
    db: Session = Depends(get_db)
):
    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    db.delete(interaction)
    db.commit()

    return {
        "message": "Interaction deleted successfully",
        "interaction_id": interaction_id
    }