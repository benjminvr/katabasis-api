from pydantic import BaseModel

class SelectNPCRequest(BaseModel):
    npc_name: str
