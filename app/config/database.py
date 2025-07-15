from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, User, Chatroom, Message


engine = create_engine("sqlite:///./gemini.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def create_tables():
    Base.metadata.create_all(bind=engine)
