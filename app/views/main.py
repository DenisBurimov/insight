import os
from pathlib import Path
from datetime import datetime
import sqlalchemy as sa
from flask import Blueprint, request, render_template
from config import config
from app import db, forms as f
import models as m
from app.services.gpt import gpt_service
from app.logger import log


main_blueprint = Blueprint("main", __name__)

CFG = config()


BASE_DIR = Path(__file__).resolve().parent.parent
folder_path = os.path.join(BASE_DIR, CFG.PAYMENTS_SOURCE_FOLDER)


@main_blueprint.route("/", methods=["GET"])
def index():
    log(log.INFO, "Main mage")

    payments_images = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            payments_images.append(filename)
    return render_template("index.html", payments_images=payments_images)


@main_blueprint.route("/preview", methods=["GET", "POST"])
def preview():
    log(log.INFO, "Preview route method: %s", request.method)

    form: f.PaymentForm = f.PaymentForm()
    if request.method == "GET":
        filename = request.args.get("filename")
        recognition = request.args.get("recognition")
        if not filename:
            log(log.ERROR, "Error rendering a preview")

        payment_query = sa.select(m.Payment).where(m.Payment.filename == filename)
        payment = db.session.scalar(payment_query)

        if recognition:
            if payment:
                log(log.INFO, "New recognition started for payment: %s", payment)
                now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                payment.filename = f"deleted_{now}_{filename}"
                db.session.commit()
                log(log.INFO, "%s marked as deleted", payment)
            else:
                log(log.INFO, "No saved payment found. Starting recognition...")

            file_path = os.path.join(folder_path, filename)

            if not os.path.exists(file_path):
                log(log.ERROR, "File does not exist %s", file_path)
                print(f"File {filename} not found")

            data, response_text = gpt_service.recognize(file_path)

            try:
                if data:
                    payment = m.Payment(**data)
                    payment.filename = filename
                if response_text:
                    payment = m.Payment(text_data=response_text)
                    payment.filename = filename
                if payment:
                    db.session.add(payment)
                    db.session.commit()
                    log(log.INFO, "New payment saved: %s", payment)
                else:
                    log(log.ERROR, "No proper data to save payment")
            except Exception as e:
                log(log.ERROR, "Failed to save payment. %s", e)

            return render_template(
                "components/details.html",
                filename=filename,
                payment=payment,
                form=form,
            )

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
