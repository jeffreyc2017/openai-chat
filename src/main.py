from model_selector import choose_model
from prompt_creator import choose_prompt
from chat_handler import chat as completions_chat
from assistants.assistant import chat as assistant_chat

def chat_completions():
    while True:
        model = choose_model()

        # Unpack returned values from choose_prompt
        instructions, name, run_instructions = choose_prompt()

        # Check if any value is None to determine if we should exit
        if instructions is None or name is None or run_instructions is None:
            print("Exiting the application.")
            return

        # Call chat with the additional parameters
        if not completions_chat(system_prompt=instructions, model=model):
            print("Exiting the application.")
            return

def assistant():
    while True:
        model = choose_model()

        # Unpack returned values from choose_prompt
        instructions, name, run_instructions = choose_prompt()

        # Check if any value is None to determine if we should exit
        if instructions is None or name is None or run_instructions is None:
            print("Exiting the application.")
            return

        if not assistant_chat(name=name, instructions=instructions, run_instructions=run_instructions, model=model):
            print("Exiting the application.")
            return

def main():
    while True:
        chat_completions_or_assistant = input("Chat completions(C/c) or Assistant(A/a)?:")
        model = choose_model()

        # Unpack returned values from choose_prompt
        instructions, name, run_instructions = choose_prompt()

        # Check if any value is None to determine if we should exit
        if instructions is None or name is None or run_instructions is None:
            print("Exiting the application.")
            return

        if chat_completions_or_assistant.lower() == 'a':
            if not assistant_chat(name=name, instructions=instructions, run_instructions=run_instructions, model=model):
                print("Exiting the application.")
                return
        elif chat_completions_or_assistant.lower() == 'c':
            if not completions_chat(system_prompt=instructions, model=model):
                print("Exiting the application.")
                return

if __name__ == "__main__":
    main()
