from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.delivery import Delivery
    from app.db.models.delivery_person import DeliveryPerson

class DeliveryAttempt(Base):
    __tablename__ = "delivery_attempts"

    attempt_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    delivery_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("deliveries.delivery_id"),
        nullable=False,
    )

    delivery_person_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("delivery_persons.delivery_person_id"),
    )

    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    failure_reason: Mapped[str | None] = mapped_column(
        String(255),
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    delivery: Mapped["Delivery"] = relationship(
        back_populates="attempts"
    )

    delivery_person: Mapped["DeliveryPerson | None"] = relationship(
        back_populates="attempts"
    )