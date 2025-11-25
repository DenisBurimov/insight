from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class MessageForm(FlaskForm):
    content = StringField("content")
    submit = SubmitField("Send")
