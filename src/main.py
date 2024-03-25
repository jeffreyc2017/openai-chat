from model_selector import choose_model
from prompt_creator import choose_prompt
from chat_handler import chat as completions_chat
from assistants.assistant import chat as assistant_chat

def main():
    while True:
        chat_completions_or_assistant = input("Chat completions(C/c) or Assistant(A/a)?:")
        streaming_enabled = input("Enable streaming?(Y/y):").lower() == 'y'
        model = choose_model()

        # Unpack returned values from choose_prompt
        name, instructions, run_instructions = choose_prompt()

        # Check if any value is None to determine if we should exit
        if instructions is None or name is None or run_instructions is None:
            print("Exiting the application.")
            return

        if chat_completions_or_assistant.lower() == 'a':
            if not assistant_chat(name=name, instructions=instructions, run_instructions=run_instructions, model=model, streaming_enabled=streaming_enabled):
                print("Exiting the application.")
                return
        elif chat_completions_or_assistant.lower() == 'c':
            if not completions_chat(system_prompt=instructions, model=model, stream_enabled=streaming_enabled):
                print("Exiting the application.")
                return
        else:
            return

if __name__ == "__main__":
    main()
