from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from datetime import datetime
from app.config.database import db
from app.models.models import Chatroom, User, Message
from app.utils.auth import get_current_user
from app.utils.gemini import get_gemini_reply


chat_router = APIRouter()

class ChatroomCreate(BaseModel):
    name: str

class ChatMessageRequest(BaseModel):
    message: str

@chat_router.post("/chatroom")
def create_chatroom(data: ChatroomCreate, user=Depends(get_current_user)):
    chatroom = Chatroom(name=data.name, user_id=user.id)
    db.add(chatroom)
    db.commit()
    return {"id": chatroom.id, "name": chatroom.name}

@chat_router.get("/chatroom")
def list_chatrooms(user=Depends(get_current_user)):
    chatrooms = db.query(Chatroom).filter(Chatroom.user_id == user.id).all()
    return [{"id": c.id, "name": c.name} for c in chatrooms]

@chat_router.post("/chatroom/{chatroom_id}/message")
def send_message(
    chatroom_id: int,
    data: ChatMessageRequest,
    user=Depends(get_current_user)
):
    chatroom = db.query(Chatroom).filter(Chatroom.id == chatroom_id, Chatroom.user_id == user.id).first()
    if not chatroom:
        raise HTTPException(status_code=404, detail="Chatroom not found")

    today = datetime.utcnow().strftime("%Y-%m-%d")
    if user.plan == "basic":
        if user.message_date != today:
            user.messages_sent = 0
            user.message_date = today
        if user.messages_sent >= 5:
            raise HTTPException(status_code=429, detail="Daily message limit (5) reached. Upgrade to Pro.")
        user.messages_sent += 1
        db.commit()

    # Save user message
    user_msg = Message(chatroom_id=chatroom.id, sender="user", content=data.message)
    db.add(user_msg)

    # Simulated Gemini reply
    gemini_text = get_gemini_reply(data.message)

    # Save AI message
    ai_msg = Message(chatroom_id=chatroom.id, sender="gemini", content=gemini_text)
    db.add(ai_msg)

    db.commit()

    return {
        "chatroom_id": chatroom.id,
        "user_message": data.message,
        "gemini_reply": gemini_text
    }

@chat_router.get("/chatroom/{chatroom_id}/history")
def get_chat_history(chatroom_id: int, user=Depends(get_current_user)):
    chatroom = db.query(Chatroom).filter(Chatroom.id == chatroom_id, Chatroom.user_id == user.id).first()
    if not chatroom:
        raise HTTPException(status_code=404, detail="Chatroom not found")

    messages = db.query(Message).filter(Message.chatroom_id == chatroom.id).order_by(Message.timestamp.asc()).all()
    return [
        {
            "sender": msg.sender,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in messages
    ]
