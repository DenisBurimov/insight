from typing import Any

import sqlalchemy as sa
from fastapi import APIRouter, Depends, Header, Request, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models as m
from api.database import get_db
from app.logger import log

router = APIRouter()


# ── Pydantic request/response schemas ─────────────────────────────────────────

class ToolCallParams(BaseModel):
    name: str | None = None
    arguments: dict[str, Any] = {}


class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: int | str | None = None
    method: str = ""
    params: ToolCallParams | None = None


class ContentItem(BaseModel):
    type: str = "text"
    text: str


class MCPResult(BaseModel):
    content: list[ContentItem] | None = None
    tools: list[dict] | None = None
    protocolVersion: str | None = None
    capabilities: dict | None = None
    serverInfo: dict | None = None
    error: dict | None = None


class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: int | str | None = None
    result: MCPResult


# ── Tool definitions ───────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "get_payments",
        "description": "List all recognized payment documents, optionally filtered by payer or recipient name.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "payer_name": {"type": "string", "description": "Filter by payer name (partial match)"},
                "recipient_name": {"type": "string", "description": "Filter by recipient name (partial match)"},
                "limit": {"type": "integer", "description": "Max results to return (default 100, max 500)"},
            },
        },
    },
    {
        "name": "get_payment",
        "description": "Get details of a single payment document by its ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "Payment ID"},
            },
            "required": ["id"],
        },
    },
]


# ── Tool handlers ──────────────────────────────────────────────────────────────

def _handle_get_payments(session: Session, args: dict) -> str:
    stmt = sa.select(m.Payment)
    if args.get("payer_name"):
        stmt = stmt.where(m.Payment.payer_name.ilike(f"%{args['payer_name']}%"))
    if args.get("recipient_name"):
        stmt = stmt.where(m.Payment.recipient_name.ilike(f"%{args['recipient_name']}%"))
    limit = min(int(args.get("limit", 100)), 500)
    stmt = stmt.order_by(m.Payment.created_at.desc()).limit(limit)
    rows = session.scalars(stmt).all()

    lines = ["id,filename,number,payment_date,summ,payer_name,payer_iban,recipient_name,recipient_iban,payment_purpose"]
    for r in rows:
        purpose = (r.payment_purpose or "").replace(",", " ")
        lines.append(
            f"{r.id},{r.filename},{r.number or ''},{r.payment_date or ''},"
            f"{r.summ or ''},{r.payer_name or ''},{r.payer_iban or ''},"
            f"{r.recipient_name or ''},{r.recipient_iban or ''},{purpose}"
        )
    return "\n".join(lines)


def _handle_get_payment(session: Session, args: dict) -> str:
    payment = session.scalar(sa.select(m.Payment).where(m.Payment.id == int(args["id"])))
    if not payment:
        return "Payment not found"
    fields = [
        f"id: {payment.id}",
        f"filename: {payment.filename}",
        f"number: {payment.number}",
        f"payment_date: {payment.payment_date}",
        f"receiving_date: {payment.receiving_date}",
        f"summ: {payment.summ}",
        f"summ_words: {payment.summ_words}",
        f"payment_purpose: {payment.payment_purpose}",
        f"payer_name: {payment.payer_name}",
        f"payer_code: {payment.payer_code}",
        f"payer_bank_name: {payment.payer_bank_name}",
        f"payer_iban: {payment.payer_iban}",
        f"recipient_name: {payment.recipient_name}",
        f"recipient_code: {payment.recipient_code}",
        f"recipient_bank_name: {payment.recipient_bank_name}",
        f"recipient_iban: {payment.recipient_iban}",
    ]
    return "\n".join(fields)


# ── Routes ─────────────────────────────────────────────────────────────────────

@router.get("")
def mcp_ping() -> dict:
    log(log.INFO, "MCP: GET /mcp — health ping")
    return {"status": "ok"}


@router.post("", response_model=MCPResponse)
def mcp(
    request: Request,
    body: MCPRequest,
    session: Session = Depends(get_db),
    authorization: str = Header(default="", alias="Authorization"),
):
    log(log.INFO, "MCP: POST %s | body: %.200s", request.url.path, body.model_dump_json())

    method = body.method
    params = body.params or ToolCallParams()
    id_ = body.id

    def ok(result: MCPResult) -> MCPResponse:
        return MCPResponse(jsonrpc="2.0", id=id_, result=result)

    def text(content: str) -> MCPResponse:
        return ok(MCPResult(content=[ContentItem(type="text", text=content)]))

    if method == "initialize":
        return ok(MCPResult(
            protocolVersion="2024-11-05",
            capabilities={"tools": {}},
            serverInfo={"name": "insight-mcp", "version": "1.0.0"},
        ))

    if method and method.startswith("notifications/"):
        return Response(status_code=202)

    log(log.INFO, "MCP: POST %s -> 200", request.url.path)

    if method == "tools/list":
        log(log.INFO, "MCP: tools/list -> %d tools", len(TOOLS))
        return ok(MCPResult(tools=TOOLS))

    if method == "tools/call":
        name = params.name
        args = params.arguments
        log(log.INFO, "MCP: tools/call name=%s args=%s", name, args)
        if name == "get_payments":
            return text(_handle_get_payments(session, args))
        if name == "get_payment":
            return text(_handle_get_payment(session, args))
        log(log.WARNING, "MCP: unknown tool %r", name)
        return ok(MCPResult(error={"code": -32601, "message": f"Unknown tool: {name}"}))

    log(log.WARNING, "MCP: method not found: %r", method)
    return ok(MCPResult(error={"code": -32601, "message": "Method not found"}))
