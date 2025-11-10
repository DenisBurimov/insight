import os
from pathlib import Path
import sqlalchemy as sa
from flask import Blueprint, request, render_template
from config import config
from app import db, models as m, forms as f
from app.services.gpt import ChatGPT
from app.logger import log


main_blueprint = Blueprint("main", __name__)

CFG = config()
gpt = ChatGPT()


BASE_DIR = Path(__file__).resolve().parent.parent


@main_blueprint.route("/", methods=["GET"])
def index():
    log(log.INFO, "Main mage")

    folder_path = os.path.join(BASE_DIR, CFG.PAYMENTS_SOURCE_FOLDER)
    payments_images = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            payments_images.append(filename)
    return render_template("index.html", payments_images=payments_images)


@main_blueprint.route("/preview", methods=["GET", "POST"])
def preview():
    log(log.INFO, "Preview route method: %s", request.method)

    form: f.PaymentForm = f.PaymentForm
    if request.method == "GET":
        filename = request.args.get("filename")
        if not filename:
            log(log.ERROR, "Error rendering a preview")

        payment_query = sa.select(m.Payment).where(m.Payment.filename == filename)
        payment = db.session.scalar(payment_query)

        log(
            log.INFO, "Rendering a preview filename: %s, payment: %s", filename, payment
        )

    if form.validate_on_submit():
        pass

    return render_template(
        "components/preview.html",
        filename=filename,
        payment=payment,
        form=form,
    )


@main_blueprint.route("/no-content")
def no_content():
    """htmx request"""
    return "", 200
