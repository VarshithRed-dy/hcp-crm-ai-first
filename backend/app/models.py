from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    specialty = Column(String(255), nullable=True)
    territory = Column(String(255), nullable=True)
    segment = Column(String(100), nullable=True)
    preferred_channel = Column(String(100), nullable=True)


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=True)
    hcp_name = Column(String(255), nullable=True)

    interaction_type = Column(String(100), nullable=True)
    interaction_date = Column(String(50), nullable=True)
    interaction_time = Column(String(50), nullable=True)

    attendees = Column(Text, nullable=True)
    topics_discussed = Column(Text, nullable=True)
    materials_shared = Column(Text, nullable=True)
    samples_distributed = Column(Text, nullable=True)

    sentiment = Column(String(100), nullable=True)
    outcome = Column(Text, nullable=True)
    next_step = Column(Text, nullable=True)
    follow_up_date = Column(String(50), nullable=True)

    raw_notes = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AgentToolLog(Base):
    __tablename__ = "agent_tool_logs"

    id = Column(Integer, primary_key=True, index=True)
    tool_name = Column(String(255), nullable=False)
    input_payload = Column(Text, nullable=True)
    output_payload = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())