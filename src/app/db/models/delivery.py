from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.case import Case
    from app.db.models.delivery_attempt import DeliveryAttempt
    from app.db.models.delivery_person import DeliveryPerson
    from app.db.models.order import Order

class Delivery(Base):
    __tablename__ = "deliveries"

    delivery_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    order_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("orders.order_id"),
        nullable=False,
    )

    delivery_person_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("delivery_persons.delivery_person_id"),
    )

    delivery_partner: Mapped[str | None] = mapped_column(
        String(100),
    )

    tracking_number: Mapped[str | None] = mapped_column(
        String(100),
    )

    status: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
        default="ASSIGNED",
    )

    shipped_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    expected_delivery_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    delivered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    order: Mapped["Order"] = relationship(
        back_populates="deliveries"
    )

    delivery_person: Mapped["DeliveryPerson | None"] = relationship(
        back_populates="deliveries"
    )

    attempts: Mapped[list["DeliveryAttempt"]] = relationship(
        back_populates="delivery"
    )

    cases: Mapped[list["Case"]] = relationship(
        back_populates="delivery"
    )