import os
from pathlib import Path
import configparser
from openai import OpenAI

# Initialization
config_file = Path.cwd() / "config.cfg"
config = configparser.ConfigParser()
config.read(config_file)

openai_client = OpenAI(api_key=config["openai"]["api_key"])
model = config["openai"]["model"]

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
        print("AI is thinking...", end="", flush=True)

        try:
            response = openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message},
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            print("\rAI: ", end="")  # Use carriage return to overwrite "AI is thinking..." message

            for choice in response.choices:
                print(choice.message.content)
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            continue

if __name__ == "__main__":
    system_prompt = choose_prompt()
    chat(system_prompt)