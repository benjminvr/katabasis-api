# src/models/user_npc.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    
    # One-to-many relationship with UserNPC (user can have many selected NPCs)
    npcs = relationship("UserNPC", back_populates="user")

class UserNPC(Base):
    __tablename__ = 'user_npcs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    npc_name = Column(String, index=True)

    # Relationship with the User table
    user = relationship("User", back_populates="npcs")
