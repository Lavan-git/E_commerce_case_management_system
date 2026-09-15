from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.case import Case
    from app.db.models.support_agent import SupportAgent

class CaseUpdate(Base):
    __tablename__ = "case_updates"

    update_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    case_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("cases.case_id"),
        nullable=False,
    )

    updated_by_agent_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("support_agents.agent_id"),
    )

    source: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="AGENT",
    )

    old_status: Mapped[str | None] = mapped_column(
        String(25),
    )

    new_status: Mapped[str | None] = mapped_column(
        String(25),
    )

    comment: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    case: Mapped["Case"] = relationship(
        back_populates="updates"
    )

    updated_by_agent: Mapped["SupportAgent | None"] = relationship(
        back_populates="case_updates"
    )