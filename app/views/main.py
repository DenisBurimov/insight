import os
from pathlib import Path
from flask import Blueprint, request, render_template
from config import config
from app.services.gpt import ChatGPT
from app.logger import log


main_blueprint = Blueprint("main", __name__)

CFG = config()
gpt = ChatGPT()


BASE_DIR = Path(__file__).resolve().parent.parent


@main_blueprint.route("/", methods=["GET", "POST"])
def index():
    log(log.INFO, "Main mage")

    folder_path = os.path.join(BASE_DIR, CFG.PAYMENTS_SOURCE_FOLDER)
    payments_images = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            payments_images.append(filename)
    return render_template("index.html", payments_images=payments_images)


@main_blueprint.route("/no-content")
def no_content():
    """htmx request"""
    return "", 200
