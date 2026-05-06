import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

import models as m


class PaymentRepository:
    """All SQLAlchemy queries live here.

    The service layer never imports `sa.select` directly — it goes through
    this class so the query implementation can change without touching
    business logic.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, payment_id: int) -> m.Payment | None:
        return await self._session.scalar(
            sa.select(m.Payment).where(m.Payment.id == payment_id)
        )

    async def get_by_number(self, number: str) -> m.Payment | None:
        return await self._session.scalar(
            sa.select(m.Payment).where(m.Payment.number == number)
        )

    async def list(
        self,
        payer_name: str | None,
        recipient_name: str | None,
        limit: int,
    ) -> list[m.Payment]:
        stmt = sa.select(m.Payment)
        if payer_name:
            stmt = stmt.where(m.Payment.payer_name.ilike(f"%{payer_name}%"))
        if recipient_name:
            stmt = stmt.where(m.Payment.recipient_name.ilike(f"%{recipient_name}%"))
        stmt = stmt.order_by(m.Payment.created_at.desc()).limit(limit)
        result = await self._session.scalars(stmt)
        return list(result.all())

    def add(self, payment: m.Payment) -> None:
        self._session.add(payment)

    async def delete(self, payment: m.Payment) -> None:
        await self._session.delete(payment)
