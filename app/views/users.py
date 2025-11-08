from flask import Blueprint, render_template
from config import config
from app.logger import log


users_blueprint = Blueprint("users", __name__, url_prefix="/users")
CFG = config()


@users_blueprint.route("/", methods=["GET"])
async def get_all():
    log(log.INFO, "Users page started")

    users = ["testing", "data"]

    log(log.INFO, "Rendering users page...")
    return render_template(
        "index.html",
        users=users,
    )
