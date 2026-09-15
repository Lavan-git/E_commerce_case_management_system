from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.case import Case
    from app.db.models.order_item import OrderItem
    from app.db.models.refund import Refund


class Return(Base):
    __tablename__ = "returns"

    return_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    order_item_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("order_items.order_item_id"),
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        String(255),
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

    picked_up_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    order_item: Mapped["OrderItem"] = relationship(
        back_populates="returns"
    )

    refunds: Mapped[list["Refund"]] = relationship(
        back_populates="return_record"
    )

    cases: Mapped[list["Case"]] = relationship(
        back_populates="return_record"
    )