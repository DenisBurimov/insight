from flask import Blueprint, Response, jsonify, request
from config import config
from app.logger import log


api_payments_blueprint = Blueprint("api_payments", __name__)

CFG = config()


@api_payments_blueprint.route("/sync", methods=["GET"])
async def sync() -> tuple[Response, int]:
    log(log.INFO, "GET /payments/sync from %s", request.remote_addr)

    if not request.headers.get("Access-Token") == CFG.SCHEDULER_ACCESS_TOKEN:
        log(log.WARNING, "GET /payments/sync — access denied (bad or missing token)")
        return (jsonify({"message": "Access denied", "data": []}), 403)

    log(log.INFO, "GET /payments/sync — authorized, returning 200")
    return (
        jsonify({"message": "Sample endpoint"}),
        200,
    )
