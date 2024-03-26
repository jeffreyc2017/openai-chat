import json
import os

def get_conversation_dir(username):
    return f"./conversations/{username}"

def save_conversation(username, conversation_id, conversation_data):
    directory = get_conversation_dir(username)
    os.makedirs(directory, exist_ok=True)
    with open(f"{directory}/{conversation_id}.json", "w") as file:
        json.dump(conversation_data, file)

def load_conversation(username, conversation_id):
    try:
        with open(f"{get_conversation_dir(username)}/{conversation_id}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def list_user_conversations(username):
    directory = get_conversation_dir(username)
    try:
        return [filename for filename in os.listdir(directory) if filename.endswith('.json')]
    except FileNotFoundError:
        return []
