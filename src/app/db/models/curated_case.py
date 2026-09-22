from datetime import datetime

from sqlalchemy import DateTime, BigInteger, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CuratedCase(Base):
    __tablename__ = "curated_cases"

    curated_case_id: Mapped[int] = mapped_column(
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

    case_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    actor_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    actor_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    case_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    source_created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    curated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )