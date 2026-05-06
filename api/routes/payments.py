from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.repositories.payment_repo import PaymentRepository
from api.schemas.payment import PaymentCreate, PaymentFilters, PaymentResponse
from api.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["payments"])


# ── Dependency factory ─────────────────────────────────────────────────────────

def get_payment_service(session: AsyncSession = Depends(get_db)) -> PaymentService:
    """Wire session → repository → service.

    Routes declare this as a dependency; they never instantiate services
    directly, keeping the web layer decoupled from construction details.
    """
    repo = PaymentRepository(session)
    return PaymentService(session=session, repo=repo)


# ── Web layer ──────────────────────────────────────────────────────────────────
# Handlers do three things only:
#   1. Declare what comes in (path params, query params, request body)
#   2. Call the service
#   3. Return the response
# No business logic, no SQL, no domain decisions.

@router.get("", response_model=list[PaymentResponse])
async def list_payments(
    filters: Annotated[PaymentFilters, Query()],
    service: PaymentService = Depends(get_payment_service),
) -> list[PaymentResponse]:
    return await service.list_payments(filters)  # type: ignore[return-value]


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:
    return await service.get_payment(payment_id)  # type: ignore[return-value]


@router.post("", response_model=PaymentResponse, status_code=201)
async def create_payment(
    body: PaymentCreate,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:
    return await service.create_payment(body)  # type: ignore[return-value]


@router.delete("/{payment_id}", status_code=204)
async def delete_payment(
    payment_id: int,
    service: PaymentService = Depends(get_payment_service),
) -> None:
    await service.delete_payment(payment_id)
