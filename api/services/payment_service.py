from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

import models as m
from api.domain.errors import DuplicatePaymentNumber, InvalidPaymentAmount, PaymentNotFound
from api.repositories.payment_repo import PaymentRepository
from api.schemas.payment import PaymentCreate, PaymentFilters


class PaymentService:
    """Pure business logic — no FastAPI, no HTTP, no SQLAlchemy queries.

    This class answers the interview question "where is business logic":
    - validates domain rules (unique number, positive amount)
    - owns transaction boundaries (commit / rollback)
    - raises domain errors that the web layer translates to HTTP responses
    """

    def __init__(self, session: AsyncSession, repo: PaymentRepository) -> None:
        self._session = session
        self._repo = repo

    # ── Queries ────────────────────────────────────────────────────────────────

    async def list_payments(self, filters: PaymentFilters) -> list[m.Payment]:
        return await self._repo.list(
            payer_name=filters.payer_name,
            recipient_name=filters.recipient_name,
            limit=filters.limit,
        )

    async def get_payment(self, payment_id: int) -> m.Payment:
        payment = await self._repo.get_by_id(payment_id)
        if payment is None:
            raise PaymentNotFound(payment_id)
        return payment

    # ── Commands ───────────────────────────────────────────────────────────────

    async def create_payment(self, data: PaymentCreate) -> m.Payment:
        # Business rule: payment numbers must be unique
        if data.number:
            existing = await self._repo.get_by_number(data.number)
            if existing:
                raise DuplicatePaymentNumber(data.number)

        # Business rule: if a numeric amount is provided it must be positive
        if data.summ is not None:
            try:
                amount = float(data.summ.replace(",", "."))
            except ValueError:
                amount = None
            if amount is not None and amount <= 0:
                raise InvalidPaymentAmount(f"Payment amount must be positive, got {data.summ!r}")

        now = datetime.now(timezone.utc)
        payment = m.Payment(
            **data.model_dump(),
            created_at=now,
            updated_at=now,
        )
        self._repo.add(payment)

        # Transaction boundary: the commit lives in the service, not the route.
        # If anything above raised, the session is rolled back by get_db().
        await self._session.commit()
        await self._session.refresh(payment)
        return payment

    async def delete_payment(self, payment_id: int) -> None:
        payment = await self._repo.get_by_id(payment_id)
        if payment is None:
            raise PaymentNotFound(payment_id)

        await self._repo.delete(payment)
        await self._session.commit()
