from flask import Blueprint, request, render_template
from flask_login import current_user, login_required
from app.services.chat import get_history_messages, get_room, save_message_assistant, save_message_user
from app import forms as f
from app.services.gpt import gpt_service
from app.logger import log


chat_blueprint = Blueprint("chat", __name__, url_prefix="/chat")


@chat_blueprint.route("/get_history", methods=["GET"])
@login_required
def get_history():
    log(log.INFO, "Chat history route")
    room = get_room(current_user.id)
    
    messages = get_history_messages(room.id)
    log(log.INFO, "Fetched %d messages for room %s", len(messages), room.id)
    
    return render_template("chat/history.html", messages=messages)

@chat_blueprint.route("/send_message", methods=["POST", "GET"])
def send_message():
    log(log.INFO, "Send message route")
    form = f.MessageForm(request.args if request.method == "GET" else request.form, meta={'csrf': False})
    if not form.validate():
        log(log.WARNING, "Invalid data form errors: %s", form.errors)
        return {"error": "Invalid input"}, 400
    
    content = form.content.data
    log(log.INFO, "Received message from user %s: %s", current_user.id, content)
    room = get_room(current_user.id)

    messages = []
    
    user_message = save_message_user(room.id, content)
    messages.append(user_message)
    
    assistant_response = gpt_service.get_answer(content)
    log(log.INFO, "Received assistant response: %s", assistant_response)
    
    assistant_message = save_message_assistant(room.id, assistant_response)
    messages.append(assistant_message)

    return render_template("chat/history.html", messages=messages)