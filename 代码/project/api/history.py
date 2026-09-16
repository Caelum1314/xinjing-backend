from fastapi import APIRouter
from utils.storage import load_chat_history

router = APIRouter()

@router.get("/get_chat_history")
async def get_chat_history():
    return {"history": load_chat_history()}

@router.post("/clear_chat_history")
async def clear_chat_history():
    import os
    from config import CHAT_FILE
    if os.path.exists(CHAT_FILE):
        os.remove(CHAT_FILE)
    return {"status": "ok"}