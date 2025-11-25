from datetime import datetime
import sqlalchemy as sa
from app import db, models as m
from app.logger import log

def get_room(user_id: int) -> m.Room:
    room = db.session.scalar(
        sa.select(m.Room).where(m.Room.user_id == user_id)
    )
    if not room:
        log(log.INFO, "No chat room found for user %s", user_id)

        room = m.Room(
            user_id=user_id,
            name=f"Chat Room {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ).save()
        m.Message(
            room_id=room.id,
            sender=m.MessageSender.ASSISTANT.value,
            content="Hello! How can I assist you today?",
        ).save()
        log(log.INFO, "Created new chat room %s for user %s", room.id, user_id)
    return room

def get_history_messages(room_id: int) -> list[m.Message]:
    messages = db.session.scalars(
        sa.select(m.Message).where(m.Message.room_id == room_id).order_by(m.Message.created_at)
    ).all()
    return messages

def save_message_user(room_id: int, content: str) -> m.Message:
    user_message = m.Message(
        room_id=room_id,
        role=m.MessageSender.USER.value,
        content=content,
    ).save()
    log(log.INFO, "Saved user message %s", user_message.id)
    return user_message

def save_message_assistant(room_id: int, content: str) -> m.Message:
    assistant_message = m.Message(
        room_id=room_id,
        role=m.MessageSender.ASSISTANT.value,
        content=content,
    ).save()
    log(log.INFO, "Saved assistant message %s", assistant_message.id)
    return assistant_message