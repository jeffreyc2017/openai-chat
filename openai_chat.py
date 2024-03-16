import os
from pathlib import Path
import configparser
from openai import OpenAI
import tiktoken

# Initialization
config_file = Path.cwd() / "config.cfg"
config = configparser.ConfigParser()
config.read(config_file)

openai_client = OpenAI(api_key=config["openai"]["api_key"])
model = config["openai"]["model"]

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """
    Return the number of tokens used by a list of messages.
    https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def choose_prompt():
    prompts = [
        "You are an assistant.",
        "You are a friend giving advice.",
        "You are a tutor explaining a concept.",
        "You are a coach motivating your team.",
        "You are a traveler sharing stories."
    ]
    
    print("Choose a conversation starter:")
    for i, prompt in enumerate(prompts, start=1):
        print(f"{i}. {prompt}")
    print("Select a number or press enter for a random start.")

    choice = input("Your choice: ")
    try:
        chosen_index = int(choice) - 1
        if chosen_index in range(len(prompts)):
            return prompts[chosen_index]
        else:
            raise ValueError
    except ValueError:
        print("Invalid choice, proceeding with a random prompt.")
        return "You are an assistant."

def chat(system_prompt):
    """
    This function continuously accepts user input, breaks it into lines, and then sends it to
    OpenAI's chat completion API to generate a response based on the provided model.
    The conversation starts with the system stating "You are a good friend.".
    """
    print("\nEnter your message. Press enter twice to send. Type 'exit' to quit.")
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

        message = "\n".join(user_input)
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ]

        print(f"{num_tokens_from_messages(messages, model)} prompt tokens counted.")
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
            print("\rAI: ", end="")  # Use carriage return to overwrite "AI is thinking..." message

            for choice in response.choices:
                print(choice.message.content)

            print(f'{response.usage.prompt_tokens} prompt tokens counted by the OpenAI API.')
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            continue

if __name__ == "__main__":
    system_prompt = choose_prompt()
    chat(system_prompt)