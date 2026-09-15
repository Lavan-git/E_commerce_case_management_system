from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.case import Case
    from app.db.models.vendor_product import VendorProduct
    from app.db.models.vendor_payout import VendorPayout
class Vendor(Base):
    __tablename__ = "vendors"

    vendor_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    business_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    legal_name: Mapped[str | None] = mapped_column(
        String(200),
    )

    email: Mapped[str] = mapped_column(
        String(254),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
    )

    gstin: Mapped[str | None] = mapped_column(
        String(15),
    )

    pan: Mapped[str | None] = mapped_column(
        String(10),
    )

    kyc_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE",
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    vendor_products: Mapped[list["VendorProduct"]] = relationship(
        back_populates="vendor"
    )

    payouts: Mapped[list["VendorPayout"]] = relationship(
        back_populates="vendor"
    )

    cases: Mapped[list["Case"]] = relationship(
        back_populates="vendor"
    )