import os
import stripe
from fastapi import APIRouter, Depends, HTTPException
from app.utils.auth import get_current_user
from dotenv import load_dotenv

load_dotenv()

payment_router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PRICE_ID = os.getenv("STRIPE_PRICE_ID")

@payment_router.post("/payment/checkout")
def create_checkout_session(user=Depends(get_current_user)):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": PRICE_ID, "quantity": 1}],
            mode="payment",
            success_url="http://localhost:8000/payment/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8000/payment/cancel",
            metadata={"user_phone": user.phone}
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@payment_router.get("/payment/success")
def payment_success():
    return {"message": "Payment successful. You're now a Pro user!"}

@payment_router.get("/payment/cancel")
def payment_cancel():
    return {"message": "Payment was cancelled."}
