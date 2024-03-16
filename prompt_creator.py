def choose_prompt():
    """
    Allows the user to select a system prompt from a predefined list.
    """
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

def format_user_input(user_input):
    """
    Formats the user input into a structured message for the OpenAI API.
    """
    return "\n".join(user_input)