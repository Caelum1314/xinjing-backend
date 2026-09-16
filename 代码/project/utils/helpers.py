from collections import deque

user_conversations = {}

def get_user_history(user_id="default", max_length=20):
    if user_id not in user_conversations:
        user_conversations[user_id] = deque(maxlen=max_length)
    return user_conversations[user_id]

def add_to_history(user_id, role, content):
    history = get_user_history(user_id)
    history.append({"role": role, "content": content})

def clear_user_history(user_id="default"):
    if user_id in user_conversations:
        user_conversations[user_id].clear()