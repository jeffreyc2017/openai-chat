def choose_prompt():
    """
    Allows the user to select a system prompt from a predefined, categorized list or enter their own.
    """
    categories = {
        "Custom": "Enter your own prompt.",
        "Education": [
            "Learn about mathematics concepts.",
            "Explore scientific phenomena.",
            "Practice a new language."
        ],
        "Entertainment": [
            "Hear a random joke.",
            "Listen to a travel story.",
            "Learn an interesting fact."
        ],
        "Professional Assistance": [
            "Assist with programming tasks.",
            "Help with Site Reliability Engineering (SRE) issues.",
            "Guide on DevOps best practices."
        ],
        "Writing & Content Creation": [
            "Generate a tweet for Twitter.",
            "Compose a blog post.",
            "Craft a README file.",
            "Write an article.",
            "Construct an essay."
        ],
        "Translator Roles": [
            "Proofread a translated text for accuracy.",
            "Translate a message from English to Chinese.",
            "Translate a message from Chinese to English."
        ],
        "English Language Assistance": [
            "Revise the content to improve clarity and coherence.",
            "Fix syntax and spelling issues within the provided content.",
            "Highlight and correct grammatical errors in the text."
        ],
        "English Teacher": [
            """Identify any grammatical errors in the user’s input before responding. 
            Praise the user for correct grammar if no issues are found.""",
            "Offer explanations for common English language mistakes.",
            "Provide feedback on language use and suggest improvements."
        ],
        "Website Content Analysis": "Analyze content from a website URL.",
    }

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
    
    if chosen_category == "Website Content Analysis":
        url = input("Enter the website URL to analyze: ")
        return {"type": "website_analysis", "url": url}

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