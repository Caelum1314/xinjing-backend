from fastapi import APIRouter, File, UploadFile, Form
from services.emotion_service import analyze_emotion_from_bytes
from utils.storage import add_emotion_record, update_stats

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