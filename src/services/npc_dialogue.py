#Caching npc dialogues
from fastapi import HTTPException
from src.config.database import redis_client
from openai import AzureOpenAI
import hashlib
import json
import os

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL")
AZURE_OPENAI_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT,
    api_key = AZURE_OPENAI_API_KEY,
    api_version = AZURE_OPENAI_VERSION 
)

def chat_with_npc(user_id: str, npc_name: str, message: str):
    """Handles chat with an NPC, caching responses in Reids"""

    # Create a Redis key for user-NPC conversation 
    redis_key = f"user:{user_id}:npc:{npc_name}:chat_history"
    
    # Retrieve previous messages if they exist
    chat_history = redis_client.get(redis_key)
    chat_history = json.loads(chat_history) if chat_history else []

    #Add user message to history
    chat_history.append({"role": "user", "content":message})

    #Otherwise, call OpenAI API
    response = client.chat.completions.create(
        model = AZURE_OPENAI_MODEL,
        messages = [
            {"role": "system", "content": f"You are {npc_name}, a game NPC  and users friend."},
            *chat_history,
        ],
        max_tokens = 150,
        temperature = 0.9, #The higher the temp, the most creative the responses
        top_p = 1.0
    )

    response_text = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": response_text})

    redis_client.setex(redis_key, 1800, json.dumps(chat_history)) #Cache for 5 min

    return response_text

def get_chat_history(user_id: str, npc_name: str):
    """Fetch chat history from Redis"""
    redis_key = f"user:{user_id}:npc:{npc_name}:chat_history"

    #Get chat history from Redis
    chat_history = redis_client.get(redis_key)

    if not chat_history:
        raise HTTPException(status_code=404, detail="Chat history not found")
    
    chat_history = json.loads(chat_history)

    return chat_history