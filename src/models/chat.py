from pydantic import BaseModel

class ChatRequest(BaseModel):
    npc_name: str
    message: str