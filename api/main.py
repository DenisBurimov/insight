import os
from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi_limiter import FastAPILimiter

from api.database import warm_pool
from api.domain.errors import (
    DuplicatePaymentNumber,
    InvalidPaymentAmount,
    PaymentNotFound,
)
from api.routes import mcp_router, payments_router

_REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/2")


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(_REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)
    await warm_pool()
    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifespan)

app.include_router(mcp_router, prefix="/mcp")
app.include_router(payments_router)


# ── Domain error → HTTP status mapping ────────────────────────────────────────
# The service raises domain errors with no knowledge of HTTP.
# This is the single place that decides what status code each error maps to.


@app.exception_handler(PaymentNotFound)
async def handle_payment_not_found(
    request: Request, exc: PaymentNotFound
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(DuplicatePaymentNumber)
async def handle_duplicate_payment(
    request: Request, exc: DuplicatePaymentNumber
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(InvalidPaymentAmount)
async def handle_invalid_amount(
    request: Request, exc: InvalidPaymentAmount
) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/routes")
async def list_routes():
    return [
        {"path": route.path, "methods": sorted(route.methods), "name": route.name}
        for route in app.routes
        if isinstance(route, APIRoute)
    ]
