import cv2
import numpy as np
from deepface import DeepFace
from config import EMOTION_MAP

def analyze_emotion(img):
    try:
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False, silent=True)
        if result and len(result) > 0:
            emotion_raw = result[0]['dominant_emotion']
            confidence = float(result[0]['emotion'][emotion_raw])
            emotion_cn = EMOTION_MAP.get(emotion_raw, emotion_raw)
            return {"emotion": emotion_cn, "confidence": confidence}
    except Exception as e:
        print(f"Emotion analysis error: {e}")
    return {"emotion": "未知", "confidence": 0}

def analyze_emotion_from_bytes(file_bytes):
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return {"emotion": "未知", "confidence": 0}
    return analyze_emotion(img)