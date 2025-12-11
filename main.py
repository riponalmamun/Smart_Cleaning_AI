from fastapi import FastAPI
from routers import matching, scheduling, pricing, chatbot
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Smart Cleaning AI Platform",
    description="AI-powered platform for cleaner matching, scheduling, pricing, and chatbot",
    version="1.0"
)

# Allow frontend requests (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(matching.router)
app.include_router(scheduling.router)
app.include_router(pricing.router)
app.include_router(chatbot.router)

@app.get("/")
def root():
    return {"message": "Welcome to Smart Cleaning AI Platform 🚀"}
