from model_selector import choose_model
from prompt_creator import choose_prompt
from chat_completions.chat_handler import chat as completions_chat
from assistants.assistant import chat as assistant_chat

def main():
    while True:
        chat_completions_or_assistant = input("Chat completions(C/c) or Assistant(A/a)?:").lower()
        if chat_completions_or_assistant != 'a' and chat_completions_or_assistant != 'c':
            return
        streaming_enabled = input("Enable streaming?(Y/y):").lower() == 'y'
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
                stream_enabled=streaming_enabled
            )
        elif chat_completions_or_assistant == 'a':
            (restart, conversation_history) = assistant_chat(
                name=category_name,
                instructions=instructions,
                run_instructions=run_instructions,
                model=model,
                streaming_enabled=streaming_enabled
            )

        if not restart:
            print("Exiting the application.")
            return


if __name__ == "__main__":
    main()
