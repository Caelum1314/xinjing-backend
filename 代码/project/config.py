import os

API_KEY = "7b9c1ea933a8499990d8c7fa8b2352cd.xgWrwaq1uIU8f9m9"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

CHAT_FILE = os.path.join(DATA_DIR, "chat_history.json")
EMOTION_FILE = os.path.join(DATA_DIR, "emotion_history.json")
SURVEY_FILE = os.path.join(DATA_DIR, "survey_data.json")
ACHIEVEMENT_FILE = os.path.join(DATA_DIR, "achievements.json")

EMOTION_MAP = {
    'happy': '开心', 'sad': '悲伤', 'angry': '愤怒',
    'fear': '恐惧', 'surprise': '惊讶', 'neutral': '平静', 'disgust': '厌恶'
}

EMOTION_SCORE = {"开心": 100, "平静": 70, "惊讶": 60, "悲伤": 35, "恐惧": 30, "愤怒": 25, "厌恶": 20}

ACHIEVEMENTS = {
    "first_chat": {"name": "初次对话", "desc": "完成第一次对话", "icon": "💬", "condition": "chat_count>=1"},
    "chat_10": {"name": "倾诉者", "desc": "完成10次对话", "icon": "🗣️", "condition": "chat_count>=10"},
    "first_emotion": {"name": "情绪觉察", "desc": "第一次情绪识别", "icon": "😊", "condition": "emotion_count>=1"},
    "emotion_10": {"name": "情绪记录者", "desc": "记录10次情绪", "icon": "📊", "condition": "emotion_count>=10"},
    "survey_first": {"name": "问卷新手", "desc": "第一次提交问卷", "icon": "📋", "condition": "survey_count>=1"},
    "happy_streak_3": {"name": "阳光心态", "desc": "连续3天情绪积极", "icon": "☀️", "condition": "happy_streak>=3"},
}

SYSTEM_PROMPT = """你是心镜，一个温暖、真诚、专业的AI心理陪伴助手。

像真人朋友一样聊天，语言自然有变化，避免模板化表达。可以适当展现思考过程，让对话更有人情味。回复长度适中，简单问题简短回答，复杂问题详细分析。

你可以自由使用加粗、小标题、列表等格式让内容更清晰。"""