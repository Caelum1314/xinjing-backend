from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    enable_search: bool = False
    deep_think: bool = False
    user_id: str = "default"

class SurveyQuestion(BaseModel):
    text: str
    options: List[str]

class SurveyData(BaseModel):
    title: str
    questions: List[SurveyQuestion]

class EmotionRecord(BaseModel):
    emotion: str
    confidence: float
    source: str = "camera"