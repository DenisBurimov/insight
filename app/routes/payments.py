import os
from flask import Blueprint, Response, jsonify, request
import sqlalchemy as sa

from app import db
import models as m
from config import config
from app.logger import log


api_payments_blueprint = Blueprint("api_payments", __name__)

CFG = config()


@api_payments_blueprint.route("/sync", methods=["GET"])
async def sync() -> tuple[Response, int]:
    if not request.headers.get("Access-Token") == CFG.SCHEDULER_ACCESS_TOKEN:
        return (jsonify({"message": "Access denied", "data": []}), 403)

    return (
        jsonify({"message": "Sample endpoint"}),
        200,
    )
