from fastapi import APIRouter, Depends
from app.config.database import db
from app.models.models import User
from app.utils.auth import get_current_user

subscription_router = APIRouter()

@subscription_router.post("/subscribe/pro")
def subscribe_pro(user=Depends(get_current_user)):
    user.plan = "pro"
    db.commit()
    return {"message": "You are now a Pro user!"}

@subscription_router.get("/subscription/status")
def subscription_status(user=Depends(get_current_user)):
    return {"plan": user.plan}
