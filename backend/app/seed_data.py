from sqlalchemy.orm import Session

from app.models import HCP


def seed_hcps(db: Session):
    existing_count = db.query(HCP).count()

    if existing_count > 0:
        return

    sample_hcps = [
        HCP(
            name="Dr. Emily Smith",
            specialty="Cardiology",
            territory="Dallas",
            segment="High Value",
            preferred_channel="In-person",
            organization="Dallas Heart Center",
            last_interaction_date="2026-07-01"
        ),
        HCP(
            name="Dr. Raj Rao",
            specialty="Endocrinology",
            territory="Plano",
            segment="Medium Value",
            preferred_channel="Email",
            organization="Plano Medical Group",
            last_interaction_date="2026-06-25"
        ),
        HCP(
            name="Dr. Michael Johnson",
            specialty="Oncology",
            territory="Austin",
            segment="High Value",
            preferred_channel="Virtual Meeting",
            organization="Austin Cancer Institute",
            last_interaction_date="2026-06-20"
        ),
        HCP(
            name="Dr. Priya Patel",
            specialty="Primary Care",
            territory="Irving",
            segment="Growth",
            preferred_channel="Phone",
            organization="Irving Family Clinic",
            last_interaction_date="2026-06-15"
        )
    ]

    db.add_all(sample_hcps)
    db.commit()