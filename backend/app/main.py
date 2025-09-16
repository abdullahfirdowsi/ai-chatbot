from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.document_routes import router as document_router

app = FastAPI(
    title="AI Chatbot API",
    description="A modern AI-powered chatbot backend built with FastAPI",
    version="1.0.0",
    contact={
        "name": "AI Chatbot Support"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev; restrict in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(document_router)
