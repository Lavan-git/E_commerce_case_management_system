from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.case import Case
    from app.db.models.order import Order
    from app.db.models.return_model import Return
    from app.db.models.vendor_product import VendorProduct

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    order_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("orders.order_id"),
        nullable=False,
    )

    vendor_product_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("vendor_products.vendor_product_id"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    order: Mapped["Order"] = relationship(
        back_populates="items"
    )

    vendor_product: Mapped["VendorProduct"] = relationship(
        back_populates="order_items"
    )

    returns: Mapped[list["Return"]] = relationship(
        back_populates="order_item"
    )

    cases: Mapped[list["Case"]] = relationship(
        back_populates="order_item"
    )