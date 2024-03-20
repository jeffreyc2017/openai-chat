from model_selector import choose_model
from prompt_creator import choose_prompt
from chat_handler import chat, format_user_input
from assistants.assistant import OpenAIAssistant

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
        if not chat(system_prompt=instructions, model=model):
            print("Exiting the application.")
            return

def assistant():
    model = choose_model()

    # Unpack returned values from choose_prompt
    instructions, name, run_instructions = choose_prompt()

    # Check if any value is None to determine if we should exit
    if instructions is None or name is None or run_instructions is None:
        print("Exiting the application.")
        return

    assistant = OpenAIAssistant(
        name=name,
        instructions=instructions,
        model=model,
        streaming_enabled=True
    )

    while True:
        print("\nyou: ", end="")
        user_input = []
        while (line := input()) != "":
            if line.lower() == "exit":  # Allow the user to exit the chat
                print("Exiting chat. Goodbye!")
                return
            elif line.lower() == "restart":
                return

            user_input.append(line)

            if not user_input:  # Skip empty messages
                continue

            message = format_user_input(user_input)
            assistant.run(
                run_instructions=run_instructions,
                user_message=message
            )

if __name__ == "__main__":
    # assistant()
    chat_completions()