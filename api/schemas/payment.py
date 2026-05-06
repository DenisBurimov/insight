from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PaymentFilters(BaseModel):
    """Query-string parameters — validated before the handler body runs."""

    payer_name: str | None = None
    recipient_name: str | None = None
    limit: int = Field(default=100, ge=1, le=500)


class PaymentCreate(BaseModel):
    """Request body for POST /payments — Pydantic rejects invalid input here."""

    filename: str = Field(..., min_length=1, max_length=64)
    number: str | None = Field(default=None, max_length=64)
    payment_date: str | None = None
    receiving_date: str | None = None
    summ: str | None = None
    summ_words: str | None = None
    payment_purpose: str | None = Field(default=None, max_length=1024)
    payer_name: str | None = Field(default=None, max_length=128)
    payer_code: str | None = Field(default=None, max_length=10)
    payer_bank_name: str | None = None
    payer_iban: str | None = None
    recipient_name: str | None = Field(default=None, max_length=128)
    recipient_code: str | None = Field(default=None, max_length=10)
    recipient_bank_name: str | None = None
    recipient_iban: str | None = None


class PaymentResponse(BaseModel):
    """What the API returns — decoupled from the ORM model shape."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    number: str | None
    payment_date: str | None
    receiving_date: str | None
    summ: str | None
    summ_words: str | None
    payment_purpose: str | None
    payer_name: str | None
    payer_iban: str | None
    recipient_name: str | None
    recipient_iban: str | None
    created_at: datetime
    updated_at: datetime
