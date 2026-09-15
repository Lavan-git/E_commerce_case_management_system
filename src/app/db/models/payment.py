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
    from app.db.models.customer import Customer
    from app.db.models.order import Order
    from app.db.models.refund import Refund


class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    customer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("customers.customer_id"),
        nullable=False,
    )

    order_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("orders.order_id"),
    )

    transaction_reference: Mapped[str | None] = mapped_column(
        String(100),
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    payment_method: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
        default="PENDING",
    )

    transaction_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="payments"
    )

    order: Mapped["Order | None"] = relationship(
        back_populates="payments"
    )

    refunds: Mapped[list["Refund"]] = relationship(
        back_populates="payment"
    )

    cases: Mapped[list["Case"]] = relationship(
        back_populates="payment"
    )