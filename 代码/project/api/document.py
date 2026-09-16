from fastapi import APIRouter, File, UploadFile
from services.document_service import analyze_document

router = APIRouter()

@router.post("/analyze_document")
async def analyze_document_api(file: UploadFile = File(...)):
    contents = await file.read()
    result = analyze_document(contents, file.filename)
    return result