from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)
    plan = Column(String, default="basic")
    messages_sent = Column(Integer, default=0)
    message_date = Column(String)

class Chatroom(Base):
    __tablename__ = "chatrooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    chatroom_id = Column(Integer, ForeignKey("chatrooms.id"))
    sender = Column(String)  # 'user' or 'gemini'
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
