from pathlib import Path
import configparser
from openai import OpenAI

from model_selector import choose_model
from prompt_creator import choose_prompt, format_user_input
from token_counter import num_tokens_from_messages

# Initialization
config_file = Path.cwd() / "config.cfg"
config = configparser.ConfigParser()
config.read(config_file)

openai_client = OpenAI(api_key=config["openai"]["api_key"])

def chat(system_prompt, model):
    """
    This function continuously accepts user input, breaks it into lines, and then sends it to
    OpenAI's chat completion API to generate a response based on the provided model.
    The conversation starts with the system stating "You are a good friend.".
    """
    print("""--------------------------------
Enter your message. Press enter twice to send. Type 'exit' to quit.
""")

    while True:
        print("\nyou: ", end="")
        user_input = []
        while (line := input()) != "":
            if line.lower() == "exit":  # Allow the user to exit the chat
                print("Exiting chat. Goodbye!")
                return
            user_input.append(line)

        if not user_input:  # Skip empty messages
            continue

        message = format_user_input(user_input)
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ]

        num_tokens = num_tokens_from_messages(messages, model)
        print("AI is thinking...", end="", flush=True)

        try:
            response = openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=1,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            print("\r-------------------------\nAI: ", end="")  # Use carriage return to overwrite "AI is thinking..." message

            for choice in response.choices:
                print(choice.message.content)

            print(f'-------------------------\nToken count for this interaction: {num_tokens} (calculated), {response.usage.prompt_tokens} (API reported).')
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            continue

def main():
    model = choose_model()
    system_prompt = choose_prompt()
    chat(system_prompt, model)

if __name__ == "__main__":
    main()