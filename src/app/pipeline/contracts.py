from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


CaseType = Literal[
    "ACCOUNT",
    "ORDER",
    "PAYMENT",
    "DELIVERY",
    "RETURN",
    "REFUND",
    "PAYOUT",
    "VENDOR",
    "OTHER",
]

CasePriority = Literal[
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
]

CaseStatus = Literal[
    "OPEN",
    "IN_PROGRESS",
    "WAITING_FOR_CUSTOMER",
    "WAITING_FOR_VENDOR",
    "WAITING_FOR_EXTERNAL",
    "RESOLVED",
    "CLOSED",
    "CANCELLED",
]

ActorType = Literal[
    "CUSTOMER",
    "VENDOR",
]


class StandardizedCaseRecord(BaseModel):
    """
    Canonical representation of a case inside the data pipeline.

    Different source systems may use different names, formats,
    and data types. All source records must eventually conform
    to this contract.
    """

    model_config = ConfigDict(extra="forbid")

    case_id: int = Field(gt=0)

    actor_type: ActorType
    actor_id: int = Field(gt=0)

    case_type: CaseType
    priority: CasePriority
    status: CaseStatus

    category: str = Field(min_length=1)
    description: str = Field(min_length=1)

    created_at: datetime