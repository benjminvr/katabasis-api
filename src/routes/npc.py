from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.models.user import UserNPC, User
from src.models.npc import SelectNPCRequest
from src.services.auth import get_current_user

router = APIRouter()

@router.post("/select_npc")
async def select_npc(request: SelectNPCRequest, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    npc_name = request.npc_name
    
    # Get user_id from the user dictionary returned by get_current_user
    user_id = user["user_id"]  # Extract the user_id from the dictionary
    
    # Check if NPC already selected by this user
    npc_exists = db.query(UserNPC).filter(UserNPC.npc_name == npc_name, UserNPC.user_id == user_id).first()
    if npc_exists:
        raise HTTPException(status_code=400, detail="NPC already selected.")
    
    # Create a new NPC selection
    new_npc = UserNPC(user_id=user_id, npc_name=npc_name)
    db.add(new_npc)
    db.commit()

    return {"message": f"NPC {npc_name} selected successfully"}


