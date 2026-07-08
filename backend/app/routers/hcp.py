from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import HCP
from app.schemas import HCPCreate, HCPResponse

router = APIRouter(
    prefix="/api/hcps",
    tags=["HCPs"]
)


@router.get("/", response_model=List[HCPResponse])
def get_hcps(db: Session = Depends(get_db)):
    return db.query(HCP).order_by(HCP.name.asc()).all()


@router.get("/{hcp_id}", response_model=HCPResponse)
def get_hcp_by_id(hcp_id: int, db: Session = Depends(get_db)):
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()

    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")

    return hcp


@router.post("/", response_model=HCPResponse)
def create_hcp(payload: HCPCreate, db: Session = Depends(get_db)):
    hcp = HCP(**payload.model_dump())
    db.add(hcp)
    db.commit()
    db.refresh(hcp)
    return hcp