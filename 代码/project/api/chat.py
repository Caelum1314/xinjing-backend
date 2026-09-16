from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse
from services.ai_service import call_ai
from utils.helpers import add_to_history, get_user_history
from utils.storage import add_chat_record, update_stats

router = APIRouter()


@router.post("/chat")
async def chat(
        message: str = Form(...),
        enable_search: bool = Form(False),
        deep_think: bool = Form(False),
        user_id: str = Form("default")
):
    try:
        add_to_history(user_id, "user", message)

        history = get_user_history(user_id)
        messages = list(history)[:-1] + [{"role": "user", "content": message}]

        response = call_ai(messages, stream=True, enable_search=enable_search, deep_think=deep_think)

        async def generate():
            full_reply = ""
            for chunk in response:
                delta = chunk.choices[0].delta
                if delta.content:
                    full_reply += delta.content
                    yield delta.content

                # 开启联网检索时，把命中的搜索结果一并回传，前端可展示
                tool_calls = getattr(delta, "tool_calls", None)
                if tool_calls:
                    for tool in tool_calls:
                        if getattr(tool.function, "name", "") == "web_search":
                            yield f"\n\n🔍 搜索结果：\n{tool.function.arguments}\n"

            add_to_history(user_id, "assistant", full_reply)
            add_chat_record(message, full_reply)
            new_achievements = update_stats("chat")
            if new_achievements:
                yield f"\n\n🎉 解锁成就：{new_achievements[0]['name']}！"

        return StreamingResponse(generate(), media_type="text/event-stream")
    except Exception as e:
        print(f"Chat error: {e}")
        return {"reply": f"遇到问题: {str(e)}"}


@router.post("/clear_history")
async def clear_history(user_id: str = Form("default")):
    from utils.helpers import clear_user_history
    clear_user_history(user_id)
    return {"status": "ok"}