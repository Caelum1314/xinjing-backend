from fastapi import APIRouter
from utils.storage import load_achievements
from config import ACHIEVEMENTS

router = APIRouter()

@router.get("/get_achievements")
async def get_achievements():
    data = load_achievements()
    unlocked = [{"name": ACHIEVEMENTS[k]["name"], "desc": ACHIEVEMENTS[k]["desc"], "icon": ACHIEVEMENTS[k]["icon"]} for k in data["unlocked"] if k in ACHIEVEMENTS]
    return {"unlocked": unlocked, "stats": data["stats"]}