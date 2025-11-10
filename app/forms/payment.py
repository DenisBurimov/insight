from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class PaymentForm(FlaskForm):
    filename = StringField("filename")
    number = StringField("number")
    payment_date = StringField("payment_date")
    receiving_date = StringField("receiving_date")
    summ = StringField("summ")
    summ_words = StringField("summ_words")
    payment_purpose = StringField("payment_purpose")
    payer_name = StringField("payer_name")
    payer_code = StringField("payer_code")
    payer_bank_name = StringField("payer_bank_name")
    payer_bank_code = StringField("payer_bank_code")
    payer_iban = StringField("payer_iban")
    recipient_name = StringField("recipient_name")
    recipient_code = StringField("recipient_code")
    recipient_bank_name = StringField("recipient_bank_name")
    recipient_bank_code = StringField("recipient_bank_code")
    recipient_iban = StringField("recipient_iban")
    submit = SubmitField("Save")
