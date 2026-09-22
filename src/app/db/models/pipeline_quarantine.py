from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PipelineQuarantine(Base):
    __tablename__ = "pipeline_quarantine"

    quarantine_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    source_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    batch_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    record_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    raw_record: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    issue_codes: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
    )

    issue_messages: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )