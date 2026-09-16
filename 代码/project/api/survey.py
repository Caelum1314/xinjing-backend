from fastapi import APIRouter, Form
import json
from utils.storage import load_survey_data, save_survey_data, update_stats

router = APIRouter()


@router.post("/generate_survey")
async def generate_survey(message: str = Form(...)):
    default_survey = {
        "title": "心理健康调查问卷",
        "questions": [
            {"text": "你最近一周的情绪状态如何？", "options": ["非常好", "比较好", "一般", "不太好", "很糟糕"]},
            {"text": "你感到压力主要来自哪里？", "options": ["学业/工作", "人际关系", "家庭", "经济", "健康"]},
            {"text": "你是否有睡眠问题？", "options": ["没有", "偶尔", "经常", "总是"]}
        ]
    }
    return {"reply": json.dumps(default_survey, ensure_ascii=False)}


@router.post("/save_survey")
async def save_survey(answers: str = Form(...)):
    data = load_survey_data()
    data["surveys"].append({
        "answers": json.loads(answers),
        "timestamp": __import__('datetime').datetime.now().isoformat()
    })
    save_survey_data(data)
    update_stats("survey")
    return {"status": "ok"}


@router.get("/get_survey_data")
async def get_survey_data():
    return {"results": load_survey_data()["surveys"]}


@router.get("/get_statistics")
async def get_statistics():
    data = load_survey_data()
    surveys = data["surveys"]
    if not surveys:
        return {"has_data": False, "count": 0, "chart_data": {}}

    q1_counts = {}
    for survey in surveys:
        answers = survey.get("answers", [])
        if answers:
            q1_counts[answers[0]] = q1_counts.get(answers[0], 0) + 1

    return {
        "has_data": True,
        "count": len(surveys),
        "chart_data": {"labels": list(q1_counts.keys()), "values": list(q1_counts.values())}
    }


@router.post("/analyze_survey_text")
async def analyze_survey_text():
    from services.ai_service import call_ai
    data = load_survey_data()
    surveys = data["surveys"]
    if not surveys:
        return {"analysis": "暂无问卷数据"}

    q1_counts = {}
    for survey in surveys:
        answers = survey.get("answers", [])
        if answers:
            q1_counts[answers[0]] = q1_counts.get(answers[0], 0) + 1

    response = call_ai(
        [{"role": "user", "content": f"分析问卷结果：{q1_counts}，共{len(surveys)}份，给出简短建议"}],
        stream=False, max_tokens=200
    )
    return {"analysis": response.choices[0].message.content}