from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CaseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    raised_by_customer_id: int | None = None
    raised_by_vendor_id: int | None = None

    case_type: str = Field(min_length=1, max_length=30)
    category: str = Field(min_length=1, max_length=50)
    reason: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)

    priority: str = "MEDIUM"

    assigned_agent_id: int | None = None

    order_id: int | None = None
    order_item_id: int | None = None
    payment_id: int | None = None
    delivery_id: int | None = None
    return_id: int | None = None
    refund_id: int | None = None
    vendor_payout_id: int | None = None

    @model_validator(mode="after")
    def validate_actor(self) -> "CaseCreate":
        customer_set = self.raised_by_customer_id is not None
        vendor_set = self.raised_by_vendor_id is not None

        if customer_set == vendor_set:
            raise ValueError(
                "Exactly one of raised_by_customer_id or "
                "raised_by_vendor_id must be provided."
            )

        return self


class CaseUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str | None = None
    priority: str | None = None
    assigned_agent_id: int | None = None
    resolution: str | None = None


class CaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    case_id: int

    raised_by_customer_id: int | None
    raised_by_vendor_id: int | None

    case_type: str
    category: str
    reason: str
    description: str

    priority: str
    status: str

    assigned_agent_id: int | None

    order_id: int | None
    order_item_id: int | None
    payment_id: int | None
    delivery_id: int | None
    return_id: int | None
    refund_id: int | None
    vendor_payout_id: int | None

    resolution: str | None

    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None