from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.models.user import User
from src.models.auth import UserLogin, UserSignup
from src.services.auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/signup/")
def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username alreadu exists")
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@router.post("/login/")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    print(f"Attempting to log in with username: {user_data.username}")

    user = db.query(User).filter(User.username == user_data.username).first()

    if not user:
        print(f"User {user_data.username} not found!")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    print(f"User {user_data.username} found, checking password...")
    if not verify_password(user_data.password, user.password_hash):
        print(f"Password mismatch for user {user_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
