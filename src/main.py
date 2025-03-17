from fastapi import FastAPI
from pydantic import BaseModel
from src.routes import auth
from src.routes.chat import router as chat_router
from src.routes.npc import router as npc_routes

# Initialize FastAPI app
app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(npc_routes, prefix="/npc", tags=["npc"])

@app.get("/")
def home():
    return {"message": "AI Katabasis is running!"}
