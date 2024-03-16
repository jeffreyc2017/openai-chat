from pathlib import Path
import configparser
from openai import OpenAI

from prompt_creator import format_user_input
from token_counter import num_tokens_from_messages

_openai_client = None

def get_openai_client():
    global _openai_client
    if _openai_client is None:
        config_file = Path.cwd() / "config" / "config.cfg"
        config = configparser.ConfigParser()
        config.read(config_file)
        _openai_client = OpenAI(api_key=config["openai"]["api_key"])
    return _openai_client

def chat(system_prompt, model):
    """
    This function continuously accepts user input, breaks it into lines, and then sends it to
    OpenAI's chat completion API to generate a response based on the provided model.
    The conversation starts with the system stating "You are a good friend.".
    """

    openai_client = get_openai_client()
    total_tokens = 0
    total_response_tokens = 0

    print("""--------------------------------
Enter your message. Press enter twice to send. Type 'exit' to quit.
""")

    while True:
        print("\nyou: ", end="")
        user_input = []
        while (line := input()) != "":
            if line.lower() == "exit":  # Allow the user to exit the chat
                print("Exiting chat. Goodbye!")
                print(f'Total tokens: {total_tokens} (calculated), {total_response_tokens} (API reported).')
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
        total_tokens += num_tokens
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

            response_tokens = response.usage.prompt_tokens
            total_response_tokens += response_tokens
            print(f'-------------------------\nToken count for this interaction: {num_tokens} (calculated), {response_tokens} (API reported).')
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            continue
