import os
import json
from datetime import datetime
from constants import CHAT_HISTORY_DIR
import time
def save_chat_history(chat_id, history):
    file_path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
    with open(file_path, "w") as f:
        json.dump({
            "id": chat_id,
            "timestamp": datetime.now().isoformat(),
            "messages": history
        }, f, indent=2)

def load_chat_history(chat_id):
    file_path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            return data.get("messages", [])
    return []

def get_all_chat_sessions():
    sessions = []
    for filename in os.listdir(CHAT_HISTORY_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(CHAT_HISTORY_DIR, filename)
            with open(file_path, "r") as f:
                data = json.load(f)
                sessions.append({
                    "id": data.get("id"),
                    "timestamp": data.get("timestamp"),
                    "message_count": len(data.get("messages", []))
                })
    return sorted(sessions, key=lambda x: x["timestamp"], reverse=True)

def create_new_chat():
    return f"chat_{int(time.time())}"