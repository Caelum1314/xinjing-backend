from zhipuai import ZhipuAI
from config import API_KEY, SYSTEM_PROMPT

client = ZhipuAI(api_key=API_KEY)


def call_ai(messages, stream=True, enable_search=False, deep_think=False, max_tokens=500, temperature=0.8):
    if deep_think:
        system_prompt = SYSTEM_PROMPT + " 请进行深度思考，从多个角度分析问题，给出更丰富的见解。"
        max_tokens = 800
        temperature = 0.85
    else:
        system_prompt = SYSTEM_PROMPT
        temperature = 0.8

    full_messages = [{"role": "system", "content": system_prompt}] + messages

    if enable_search:
        return client.chat.completions.create(
            model="glm-4-flash",
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            tools=[{"type": "web_search", "web_search": {"enable": True}}]
        )
    else:
        return client.chat.completions.create(
            model="glm-4-flash",
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )