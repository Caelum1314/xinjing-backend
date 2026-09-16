from fastapi import APIRouter, File, UploadFile, Form
from services.emotion_service import analyze_emotion_from_bytes
from utils.storage import add_emotion_record, update_stats, load_emotion_history
from config import EMOTION_SCORE, EMOTION_MAP

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    result = analyze_emotion_from_bytes(contents)
    if result["emotion"] != "未知":
        add_emotion_record(result["emotion"], result["confidence"])
        update_stats("emotion")
    return result

@router.post("/record_emotion")
async def record_emotion(emotion: str = Form(...)):
    add_emotion_record(emotion, 1.0, "manual")
    update_stats("emotion")
    return {"status": "ok"}

@router.get("/emotion_trend")
async def emotion_trend():
    """基于最近 7 条情绪记录，给出情绪走势判断。"""
    emotions = load_emotion_history()
    if len(emotions) < 3:
        return {"error": "数据不足", "need": 3, "current": len(emotions)}

    scores = [EMOTION_SCORE.get(e.get("emotion", "平静"), 50) for e in emotions[-7:]]
    avg = sum(scores) / len(scores)

    if avg >= 65:
        trend, text = "positive", "积极向好"
    elif avg >= 40:
        trend, text = "stable", "平稳"
    else:
        trend, text = "negative", "需要关注"

    return {
        "prediction": trend,
        "trend_text": text,
        "predicted_score": round(avg, 1),
        "recent_scores": scores,
        "emotion_labels": EMOTION_MAP,
        "analysis": "保持良好作息",
    }