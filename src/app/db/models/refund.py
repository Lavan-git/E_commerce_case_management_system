from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.case import Case
    from app.db.models.payment import Payment
    from app.db.models.return_model import Return

class Refund(Base):
    __tablename__ = "refunds"

    refund_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    payment_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("payments.payment_id"),
        nullable=False,
    )

    return_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("returns.return_id"),
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
        default="REQUESTED",
    )

    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    payment: Mapped["Payment"] = relationship(
        back_populates="refunds"
    )

    return_record: Mapped["Return | None"] = relationship(
        back_populates="refunds"
    )

    cases: Mapped[list["Case"]] = relationship(
        back_populates="refund"
    )