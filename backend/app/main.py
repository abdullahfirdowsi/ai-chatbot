import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.document_routes import router as document_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Chatbot API",
    description="A modern AI-powered chatbot backend built with FastAPI",
    version="1.0.0",
    contact={
        "name": "AI Chatbot Support"
    }
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
if cors_origins == ["*"]:
    cors_origins = ["*"]
else:
    cors_origins = [origin.strip() for origin in cors_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(document_router)
