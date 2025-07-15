from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
from app.config.database import db
from app.models.models import User
import random

SECRET_KEY = "your-secret"
ALGORITHM = "HS256"

auth_router = APIRouter()
otp_store = {}

class SignupRequest(BaseModel):
    phone: str

class OTPVerifyRequest(BaseModel):
    phone: str
    otp: str

@auth_router.post("/signup")
def signup(req: SignupRequest):
    existing = db.query(User).filter(User.phone == req.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(phone=req.phone)
    db.add(user)
    db.commit()
    return {"message": "User created"}

@auth_router.post("/send-otp")
def send_otp(req: SignupRequest):
    otp = str(random.randint(1000, 9999))
    otp_store[req.phone] = otp
    return {"otp": otp, "message": "Use this OTP to login"}

@auth_router.post("/verify-otp")
def verify_otp(req: OTPVerifyRequest):
    valid_otp = otp_store.get(req.phone)
    if valid_otp != req.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    user = db.query(User).filter(User.phone == req.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    payload = {
        "sub": req.phone,
        "exp": datetime.utcnow() + timedelta(minutes=5)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token}
