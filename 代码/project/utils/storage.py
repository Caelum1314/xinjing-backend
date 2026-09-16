import json
import os
from datetime import datetime
from config import CHAT_FILE, EMOTION_FILE, SURVEY_FILE, ACHIEVEMENT_FILE, ACHIEVEMENTS

def load_chat_history():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, 'r') as f:
            return json.load(f)
    return []

def save_chat_history(history):
    with open(CHAT_FILE, 'w') as f:
        json.dump(history[-200:], f, ensure_ascii=False, indent=2)

def add_chat_record(user_msg, ai_msg):
    history = load_chat_history()
    history.append({
        "id": len(history) + 1,
        "user": user_msg,
        "assistant": ai_msg,
        "timestamp": datetime.now().isoformat()
    })
    save_chat_history(history)

def load_emotion_history():
    if os.path.exists(EMOTION_FILE):
        with open(EMOTION_FILE, 'r') as f:
            return json.load(f)
    return []

def save_emotion_history(history):
    with open(EMOTION_FILE, 'w') as f:
        json.dump(history[-500:], f, ensure_ascii=False, indent=2)

def add_emotion_record(emotion, confidence, source="camera"):
    history = load_emotion_history()
    history.append({
        "emotion": emotion,
        "confidence": confidence,
        "source": source,
        "timestamp": datetime.now().isoformat()
    })
    save_emotion_history(history)

def load_survey_data():
    if os.path.exists(SURVEY_FILE):
        with open(SURVEY_FILE, 'r') as f:
            return json.load(f)
    return {"surveys": []}

def save_survey_data(data):
    with open(SURVEY_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_achievements():
    if os.path.exists(ACHIEVEMENT_FILE):
        with open(ACHIEVEMENT_FILE, 'r') as f:
            return json.load(f)
    return {"unlocked": [], "stats": {"chat_count": 0, "emotion_count": 0, "survey_count": 0, "happy_streak": 0, "active_days": 0, "last_active": None}}

def save_achievements(data):
    with open(ACHIEVEMENT_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_stats(stat_type):
    data = load_achievements()
    stats = data["stats"]
    if stat_type == "chat":
        stats["chat_count"] = stats.get("chat_count", 0) + 1
    elif stat_type == "emotion":
        stats["emotion_count"] = stats.get("emotion_count", 0) + 1
    elif stat_type == "survey":
        stats["survey_count"] = stats.get("survey_count", 0) + 1
    today = datetime.now().strftime("%Y-%m-%d")
    if stats.get("last_active") != today:
        stats["last_active"] = today
        stats["active_days"] = stats.get("active_days", 0) + 1
    save_achievements(data)
    return check_achievements(data)

def check_achievements(data):
    stats = data["stats"]
    unlocked = set(data["unlocked"])
    new = []
    for key, ach in ACHIEVEMENTS.items():
        if key in unlocked:
            continue
        if ">=" in ach["condition"]:
            cond_key, cond_val = ach["condition"].split(">=")
            if stats.get(cond_key, 0) >= int(cond_val):
                unlocked.add(key)
                new.append({"name": ach["name"], "desc": ach["desc"], "icon": ach["icon"]})
    data["unlocked"] = list(unlocked)
    save_achievements(data)
    return new