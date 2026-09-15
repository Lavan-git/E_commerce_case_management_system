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
    from app.db.models.product import Product
    from app.db.models.vendor import Vendor
    from app.db.models.order_item import OrderItem

class VendorProduct(Base):
    __tablename__ = "vendor_products"

    vendor_product_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    vendor_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("vendors.vendor_id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("products.product_id"),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
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

    vendor: Mapped["Vendor"] = relationship(
        back_populates="vendor_products"
    )

    product: Mapped["Product"] = relationship(
        back_populates="vendor_products"
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="vendor_product"
    )