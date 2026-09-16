from fastapi import APIRouter
from api.chat import router as chat_router
from api.emotion import router as emotion_router
from api.speech import router as speech_router
from api.document import router as document_router
from api.survey import router as survey_router
from api.report import router as report_router
from api.history import router as history_router
from api.achievement import router as achievement_router

router = APIRouter()

router.include_router(chat_router, tags=["chat"])
router.include_router(emotion_router, tags=["emotion"])
router.include_router(speech_router, tags=["speech"])
router.include_router(document_router, tags=["document"])
router.include_router(survey_router, tags=["survey"])
router.include_router(report_router, tags=["report"])
router.include_router(history_router, tags=["history"])
router.include_router(achievement_router, tags=["achievement"])