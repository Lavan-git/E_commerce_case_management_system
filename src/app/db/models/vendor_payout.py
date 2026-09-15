from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Date,
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
    from app.db.models.vendor import Vendor


class VendorPayout(Base):
    __tablename__ = "vendor_payouts"

    payout_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    vendor_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("vendors.vendor_id"),
        nullable=False,
    )

    expected_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    actual_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
    )

    expected_payout_date: Mapped[date | None] = mapped_column(
        Date,
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    status: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
        default="PENDING",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    vendor: Mapped["Vendor"] = relationship(
        back_populates="payouts"
    )

    cases: Mapped[list["Case"]] = relationship(
        back_populates="vendor_payout"
    )