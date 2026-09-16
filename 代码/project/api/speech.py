from fastapi import APIRouter, File, UploadFile
from services.whisper_service import speech_to_text

router = APIRouter()

@router.post("/speech_to_text")
async def speech_to_text_api(file: UploadFile = File(...)):
    contents = await file.read()
    text = speech_to_text(contents)
    return {"text": text}