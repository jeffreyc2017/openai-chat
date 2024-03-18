categories = {
    "Custom": "Enter your own prompt for the system role.",
    "Chat": [
        "Act as an old friend in conversation.",
    ],
    "Entertainment": [
        "Respond to each of my inputs with a random joke related to the topic.",
        "Respond to each of my inputs with an interesting fact relevant to the topic."
    ],
    "Writing & Content Creation": [
        "Generate content for a tweet.",
        "Compose a blog post on a given topic.",
        "Create a README file for a project.",
        "Write an article on a specified subject.",
        "Construct an essay based on a prompt."
    ],
    "Translator Roles": [
        "Proofread a translated text to ensure accuracy.",
        "Translate a message from English to Chinese.",
        "Translate a message from Chinese to English."
    ],
    "English Language Assistance": [
        "Correct syntax and spelling errors in the user's input. Output the corrected content first, followed by a bullet-point list explaining each correction.",
        "Revise the user's provided content for clarity and coherence. Then, list the reasons for each revision in bullet points.",
        "Identify any grammatical errors in the user's input before responding. If there are no issues, praise the user for correct grammar. Then, continue with a normal response."
    ],
}

def choose_prompt():
    """
    Allows the user to select a system prompt from a predefined, categorized list or enter their own.
    """
    
    # Print categories
    print("\nChoose a category:")
    for i, category in enumerate(categories.keys(), start=1):
        print(f"{i}. {category}")
    category_choice = input("\nSelect a number to choose a category, or press enter to exit: ")

    # Handle category selection
    if not category_choice.strip():
        print("No category selected. Exiting.")
        return None  # Or a default prompt
    
    try:
        chosen_category = list(categories.keys())[int(category_choice) - 1]
    except (ValueError, IndexError):
        print("Invalid category choice. Exiting.")
        return None  # Or a default prompt

    # Check if the user selected the option to enter their own prompt
    if chosen_category == "Custom":
        custom_prompt = input("Enter your own system prompt: ")
        return custom_prompt

    # Print prompts within the selected category
    print(f"\n{chosen_category} Prompts:")
    for i, prompt in enumerate(categories[chosen_category], start=1):
        print(f"{i}. {prompt}")
    prompt_choice = input("\nSelect a number to choose a prompt, or press enter for a random start: ")

    # Handle prompt selection
    try:
        if prompt_choice.strip():
            chosen_prompt = categories[chosen_category][int(prompt_choice) - 1]
            return chosen_prompt
        else:
            raise ValueError  # User chose to have a random start within the category
    except (ValueError, IndexError):
        print("Invalid choice or no choice made, proceeding with a random prompt within the category.")
        # Optionally, return a random prompt from the selected category
        import random
        return random.choice(categories[chosen_category])

def format_user_input(user_input):
    """
    Formats the user input into a structured message for the OpenAI API.
    """
    return "\n".join(user_input)

# Example usage
if __name__ == "__main__":
    system_prompt = choose_prompt()
    print("\nSelected Prompt:", system_prompt if system_prompt else "No prompt selected.")