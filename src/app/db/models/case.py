from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.customer import Customer
    from app.db.models.vendor import Vendor
    from app.db.models.support_agent import SupportAgent
    from app.db.models.order import Order
    from app.db.models.order_item import OrderItem
    from app.db.models.payment import Payment
    from app.db.models.delivery import Delivery
    from app.db.models.return_model import Return
    from app.db.models.refund import Refund
    from app.db.models.vendor_payout import VendorPayout
    from app.db.models.case_update import CaseUpdate
    
class Case(Base):
    __tablename__ = "cases"

    case_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    raised_by_customer_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("customers.customer_id"),
    )

    raised_by_vendor_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("vendors.vendor_id"),
    )

    case_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="MEDIUM",
    )

    status: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
        default="OPEN",
    )

    assigned_agent_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("support_agents.agent_id"),
    )

    order_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("orders.order_id"),
    )

    order_item_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("order_items.order_item_id"),
    )

    payment_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("payments.payment_id"),
    )

    delivery_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("deliveries.delivery_id"),
    )

    return_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("returns.return_id"),
    )

    refund_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("refunds.refund_id"),
    )

    vendor_payout_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("vendor_payouts.payout_id"),
    )

    resolution: Mapped[str | None] = mapped_column(
        Text,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    customer: Mapped["Customer | None"] = relationship(
        back_populates="cases",
        foreign_keys=[raised_by_customer_id],
    )

    vendor: Mapped["Vendor | None"] = relationship(
        back_populates="cases",
        foreign_keys=[raised_by_vendor_id],
    )

    assigned_agent: Mapped["SupportAgent | None"] = relationship(
        back_populates="assigned_cases"
    )

    order: Mapped["Order | None"] = relationship(
        back_populates="cases"
    )

    order_item: Mapped["OrderItem | None"] = relationship(
        back_populates="cases"
    )

    payment: Mapped["Payment | None"] = relationship(
        back_populates="cases"
    )

    delivery: Mapped["Delivery | None"] = relationship(
        back_populates="cases"
    )

    return_record: Mapped["Return | None"] = relationship(
        back_populates="cases"
    )

    refund: Mapped["Refund | None"] = relationship(
        back_populates="cases"
    )

    vendor_payout: Mapped["VendorPayout | None"] = relationship(
        back_populates="cases"
    )

    updates: Mapped[list["CaseUpdate"]] = relationship(
        back_populates="case"
    )