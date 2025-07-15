# 💬 Gemini Backend Chat API (FastAPI + Stripe)

This project is a **full-featured backend system** built with FastAPI that allows users to:
- Sign up with OTP-based login
- Create and manage chatrooms
- Chat with **Google Gemini API**
- Track and view message history
- Upgrade to a **Pro Plan** via Stripe (sandbox)

-----------------------------------------------------------------------------------------------------------------

## 🚀 Features

✅ JWT-based Authentication (OTP via phone)  
✅ Google Gemini 2.0 AI Response (via SDK)  
✅ Chatroom & Message History per user  
✅ Daily usage limits for "basic" users (5/day)  
✅ Stripe integration for Pro Upgrade  
✅ Secure `.env`-based config  
✅ Clean RESTful APIs with Swagger UI  
✅ Deployable on Render, Railway, or Fly.io

-----------------------------------------------------------------------------------------------------------------

## 🛠️ Technologies Used

| Tech            | Description                          |
|-----------------|--------------------------------------|
| **FastAPI**     | Web framework for APIs               |
| **SQLite**      | Local DB (can switch to PostgreSQL)  |
| **SQLAlchemy**  | ORM for database models              |
| **Google Gemini API** | AI assistant for messages     |
| **Stripe API**  | Pro Plan payment handling            |
| **JWT**         | User auth with expiry-based tokens   |

-----------------------------------------------------------------------------------------------------------------

## 📁 Folder Structure

gemini-backend/
├── main.py
├── .env (not pushed to GitHub)
├── app/
│ ├── config/
│ │ └── database.py
│ ├── models/
│ │ └── models.py
│ ├── routes/
│ │ ├── auth.py
│ │ ├── chat.py
│ │ ├── payment.py
│ │ └── subscription.py
│ └── utils/
│ ├── auth.py
│ └── gemini.py



-----------------------------------------------------------------------------------------------------------------

## ⚙️ Setup Instructions (Run Locally)

### 1. Clone the Repo

```bash
git clone https://github.com/Prranav9/gemini-backend.git
cd gemini-backend

2. Create Virtual Environment

python -m venv venv
venv\Scripts\activate  # On Windows


3. Install Requirements

pip install -r requirements.txt


4. Create .env file
Create a .env file in root with:

GEMINI_API_KEY=your-google-api-key
STRIPE_SECRET_KEY=your-stripe-secret
STRIPE_PRICE_ID=your-stripe-price-id


5. Run the Server

uvicorn main:app --reload

-----------------------------------------------------------------------------------------------------------------


Visit: 

http://localhost:8000/docs to access Swagger UI
or
https://gemini-backend-d3zi.onrender.com/docs


-----------------------------------------------------------------------------------------------------------------


🧪 Test Cards (Stripe):

Use: 4242 4242 4242 4242

Any future expiry, CVC, ZIP

Stripe test mode (no real money charged)

-----------------------------------------------------------------------------------------------------------------


✅ Matches Assignment Guide

Requirement	                       Status
Language: Python (FastAPI)	        ✅ Done
Auth: OTP + JWT	                    ✅ Done
DB: SQLite (Easy switch to PG)	    ✅ Done
Gemini API	                        ✅ Integrated
Stripe Sandbox Payments	            ✅ Integrated
Queue (Optional)	                ❌ Skipped

-----------------------------------------------------------------------------------------------------------------

🛡️ Security Notes:

.env is excluded via .gitignore

All secrets loaded using python-dotenv

Tokens expire after 5 mins (default)




