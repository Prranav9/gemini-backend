from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.routes.auth import auth_router
from app.routes.chat import chat_router
from app.routes.subscription import subscription_router
from app.config.database import create_tables
from fastapi.openapi.utils import get_openapi
from app.routes.payment import payment_router

app = FastAPI(
    title="Gemini Backend Clone",
    description="Built by Pranav Mishra for assignment",
    version="1.0.0"
)

# Routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(chat_router, tags=["Chat"])
app.include_router(subscription_router, tags=["Subscription"])
app.include_router(payment_router, tags=["Payment"])

# Run DB migrations
@app.on_event("startup")
def startup():
    create_tables()

# 🛡️ Add Bearer token support to Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Gemini Backend Clone",
        version="1.0.0",
        description="Built by Pranav Mishra",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["post", "get"]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
