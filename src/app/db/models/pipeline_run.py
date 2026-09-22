from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    run_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
    )

    source_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    batch_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    source_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    standardized_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    rejected_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    already_present_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    persisted_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )