from flask import Blueprint, request, render_template
from config import config
from app.services.gpt import ChatGPT
from app.logger import log


main_blueprint = Blueprint("main", __name__)

CFG = config()
gpt = ChatGPT()


@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    log(log.INFO, "Main mage")
    return render_template("index.html")


@main_blueprint.route("/no-content")
def no_content():
    """htmx request"""
    return "", 200
