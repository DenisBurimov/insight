from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from api.domain.errors import DomainError, DuplicatePaymentNumber, InvalidPaymentAmount, PaymentNotFound
from api.routes import mcp_router, payments_router

app = FastAPI()

app.include_router(mcp_router, prefix="/mcp")
app.include_router(payments_router)


# ── Domain error → HTTP status mapping ────────────────────────────────────────
# The service raises domain errors with no knowledge of HTTP.
# This is the single place that decides what status code each error maps to.

@app.exception_handler(PaymentNotFound)
def handle_payment_not_found(request: Request, exc: PaymentNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(DuplicatePaymentNumber)
def handle_duplicate_payment(request: Request, exc: DuplicatePaymentNumber) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(InvalidPaymentAmount)
def handle_invalid_amount(request: Request, exc: InvalidPaymentAmount) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/routes")
def list_routes():
    return [
        {"path": route.path, "methods": sorted(route.methods), "name": route.name}
        for route in app.routes
        if isinstance(route, APIRoute)
    ]
