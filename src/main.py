from model_selector import choose_model
from prompt_creator import choose_prompt
from chat_completions.chat_handler import chat as completions_chat
from assistants.assistant import chat as assistant_chat
from conversations.conversations import load_conversation, save_conversation, list_user_conversations
from datetime import datetime

def main():
    username = input("Enter your username: ")
    conversation_files = list_user_conversations(username)

    print("Available conversations:")
    for index, file in enumerate(conversation_files, start=1):
        print(f"{index}. {file}")
    choice = input("Choose a conversation to resume or press Enter to start a new one: ")

    if choice.strip():
        try:
            conversation_index = int(choice) - 1
            conversation_file = conversation_files[conversation_index]
            conversation_id = conversation_file.replace('.json', '')
            conversation_history = load_conversation(username, conversation_id)
        except (ValueError, IndexError):
            print("Invalid choice. Starting a new conversation.")
            conversation_history = None
    else:
        conversation_id = datetime.now().strftime("%Y%m%dT%H%M%S")
        conversation_history = None


    while True:
        chat_completions_or_assistant = input("Chat completions(C/c) or Assistant(A/a)?:").lower()
        if chat_completions_or_assistant != 'a' and chat_completions_or_assistant != 'c':
            return
        streaming_enabled = input("Enable streaming?(Y/y):").lower() == 'y'
        model = choose_model()

        # Unpack returned values from choose_prompt
        name, instructions, run_instructions = choose_prompt()

        # Check if any value is None to determine if we should exit
        if instructions is None or name is None or run_instructions is None:
            print("Exiting the application.")
            return

        if chat_completions_or_assistant == 'c':
            (restart, conversation_history) = completions_chat(system_prompt=instructions, model=model, stream_enabled=streaming_enabled)
            save_conversation(username, conversation_id, conversation_history)
            if not restart:
                print("Exiting the application.")
                return
        elif chat_completions_or_assistant == 'a':
            (restart, conversation_history) = assistant_chat(name=name, instructions=instructions, run_instructions=run_instructions, model=model, streaming_enabled=streaming_enabled)
            save_conversation(username, conversation_id, conversation_history)
            if not restart:
                print("Exiting the application.")
                return
        else:
            return

if __name__ == "__main__":
    main()
