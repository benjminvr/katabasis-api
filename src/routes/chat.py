from fastapi import APIRouter, Depends
from src.services.auth import get_current_user
from src.services.npc_dialogue import chat_with_npc, get_chat_history
from src.models.chat import ChatRequest


router = APIRouter()

@router.post("/")
async def chat(request: ChatRequest, user: dict = Depends(get_current_user)):
    """Chat with NPC, linked to authenticated user"""
    print(f"User {user['username']} chatting with {request.npc_name}: {request.message}")
    return {"response:": chat_with_npc(user["user_id"], request.npc_name, request.message)}

@router.get("/chat_history/{npc_name}")
async def chat_history(npc_name: str, user: dict = Depends(get_current_user)):
    history = get_chat_history(user["user_id"], npc_name)

    return {"npc": npc_name, "chat_history": history}
