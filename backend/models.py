from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# CUSTOMER MESSAGE ANALYSIS
# ============================================================

class CustomerRequest(BaseModel):

    customer_name: Optional[str] = Field(
        default=None,
        description="Customer name if identifiable from the message"
    )

    pnr: Optional[str] = Field(
        default=None,
        description="Booking reference if identifiable"
    )

    flight_number: Optional[str] = Field(
        default=None,
        description="Flight number if identifiable"
    )

    intents: list[str] = Field(
        default_factory=list,
        description="Customer intents"
    )

    requested_actions: list[str] = Field(
        default_factory=list,
        description="Actions requested by the customer"
    )

    emotional_state: str = Field(
        default="calm",
        description="Customer emotional state"
    )

    follow_up_question_necessary: bool = Field(
        default=False,
        description="Whether more information is genuinely necessary"
    )

    follow_up_question: Optional[str] = Field(
        default=None,
        description="Minimum necessary follow-up question"
    )

    summary: str = Field(
        default="",
        description="Concise summary of the request"
    )


# ============================================================
# API REQUEST
# ============================================================

class ResolveRequest(BaseModel):

    message: str = Field(
        min_length=1,
        description="Customer's message"
    )


# ============================================================
# API RESPONSE
# ============================================================

class ResolveResponse(BaseModel):

    status: str

    response: str

    customer: Optional[dict] = None

    booking: Optional[dict] = None

    analysis: dict = Field(
        default_factory=dict
    )

    actions: list[str] = Field(
        default_factory=list
    )

    escalation: list[str] = Field(
        default_factory=list
    )

    sources: list[str] = Field(
        default_factory=list
    )

    ticket: Optional[dict] = None

    audit: list[dict] = Field(
        default_factory=list
    )