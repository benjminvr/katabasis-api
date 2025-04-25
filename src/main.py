from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.routes import auth
from src.routes.chat import router as chat_router
from src.routes.npc import router as npc_routes
from starlette.responses import JSONResponse


app = FastAPI()

# Configure CORS - More permissive for development
origins = [
    "http://localhost:5173",    # Vite default
    "http://localhost:3000",    # Alternative port
    "http://127.0.0.1:5173",   # Alternative localhost
    "http://127.0.0.1:3000",   # Alternative localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add OPTIONS handler for all routes
@app.options("/{full_path:path}")
async def options_handler(request: Request):
    return JSONResponse(
        status_code=200,
        content={"detail": "OK"},
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "http://localhost:5173"),
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
        },
    )

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(npc_routes, prefix="/npc", tags=["npc"])

@app.get("/")
def home():
    return {"message": "AI Katabasis is running!"}