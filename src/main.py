from model_selector import choose_model
from prompt_creator import choose_prompt
from chat_completions.chat_handler import chat as completions_chat
from assistants.assistant import chat as assistant_chat
from conversations.conversations import load_conversation, save_conversation, list_user_conversations
from datetime import datetime

def load_history() -> tuple[str, str, str]:
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
            conversation_history = []
    else:
        conversation_id = datetime.now().strftime("%Y%m%dT%H%M%S")
        conversation_history = []

    return username, conversation_id, conversation_history

def main():
    username, conversation_id, conversation_history = load_history()

    while True:
        chat_completions_or_assistant = input("Chat completions(C/c) or Assistant(A/a)?:").lower()
        if chat_completions_or_assistant != 'a' and chat_completions_or_assistant != 'c':
            return
        streaming_enabled_input = input("Enable streaming?(Y/n):").lower()
        streaming_enabled = (streaming_enabled_input == 'y') or (not streaming_enabled_input)
        model = choose_model()

        # Unpack returned values from choose_prompt
        category_name, instructions, run_instructions = choose_prompt()

        # Check if any value is None to determine if we should exit
        if instructions is None or category_name is None or run_instructions is None:
            print("Exiting the application.")
            return

        if chat_completions_or_assistant == 'c':
            (restart, conversation_history) = completions_chat(
                system_prompt=instructions,
                model=model,
                stream_enabled=streaming_enabled,
                conversation_history=conversation_history
            )
        elif chat_completions_or_assistant == 'a':
            (restart, conversation_history) = assistant_chat(
                name=category_name,
                instructions=instructions,
                run_instructions=run_instructions,
                model=model,
                streaming_enabled=streaming_enabled,
                conversation_history=conversation_history
            )

        save_conversation(username, conversation_id, conversation_history)

        if not restart:
            print("Exiting the application.")
            return


if __name__ == "__main__":
    main()
