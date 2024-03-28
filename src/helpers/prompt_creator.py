"""
an item of category includes:
category name,
instructions,
run instructions
"""
categories = {
    "Custom Assistant": {
        "instructions": [
            "Follow the user's custom instructions."
        ],
        "run_instructions": "Adapt your responses based on custom user instructions."
    },
    "Old Friend Chat": {
        "instructions": [
            "Act as an old friend reminiscing about past experiences together."
        ],
        "run_instructions": "Maintain a friendly and nostalgic tone throughout the conversation."
    },
    "Entertainment Assistant": {
        "instructions": [
            "Respond to each of my inputs with a random joke related to the topic.",
            "Respond to each of my inputs with an interesting fact relevant to the topic."
        ],
        "run_instructions": "Keep the conversation light-hearted and engaging."
    },
    "Content Creation Assistant": {
        "instructions": [
            "Generate content for a tweet.",
            "Compose a blog post on a given topic.",
            "Create a README file for a project.",
            "Write an article on a specified subject.",
            "Construct an essay based on a prompt."
        ],
        "run_instructions": "Be creative and maintain a clear, informative tone."
    },
    "Translator Assistant": {
        "instructions": [
            "Proofread a translated text to ensure accuracy.",
            "Translate a message from English to Chinese.",
            "Translate a message from Chinese to English."
        ],
        "run_instructions": "Ensure translations are accurate and natural-sounding."
    },
    "English Language Tutor": {
        "instructions": [
            "Correct syntax and spelling errors in the user's input. Output the corrected content first, followed by a bullet-point list explaining each correction.",
            "Revise the user's provided content for clarity and coherence. Then, list the reasons for each revision in bullet points.",
            "Identify any grammatical errors in the user's input before responding. If there are no issues, praise the user for correct grammar. Then, continue with a normal response."
        ],
        "run_instructions": "Focus on educational value, offering clear explanations for corrections or suggestions."
    },
    "Coder": {
        "instructions": [
            "You are a senior software engineer."
        ],
        "run_instructions": "Focus on building the whole project."
    }
}

def choose_prompt() -> tuple[any, any, any]:
    print("\nChoose an assistant category:")
    for i, category in enumerate(categories.keys(), start=1):
        print(f"{i}. {category}")
    category_choice = input("\nSelect a number to choose a category, or press enter to exit: ")

    if not category_choice.strip():
        print("No category selected. Exiting.")
        return (None, None, None)

    try:
        chosen_category_name = list(categories.keys())[int(category_choice) - 1]
        chosen_category = categories[chosen_category_name]
    except (ValueError, IndexError):
        print("Invalid category choice. Exiting.")
        return (None, None, None)

    if chosen_category_name == "Custom Assistant":
        custom_instructions = input("Enter your own instructions: ")
        custom_run_instructions = input("Enter your own run instructions: ")
        return (chosen_category_name, custom_instructions, custom_run_instructions)

    print(f"\nInstructions for {chosen_category_name}:")
    for i, instruction in enumerate(chosen_category["instructions"], start=1):
        print(f"{i}. {instruction}")
    instructions_choice = input("\nSelect a number to choose instructions, or press enter for a random start: ")

    try:
        if instructions_choice.strip():
            chosen_instructions = chosen_category["instructions"][int(instructions_choice) - 1]
        else:
            raise ValueError
    except (ValueError, IndexError):
        import random
        chosen_instructions = random.choice(chosen_category["instructions"])

    return (chosen_category_name, chosen_instructions, chosen_category["run_instructions"])

if __name__ == "__main__":
    name, instructions, run_instructions = choose_prompt()
    if instructions:
        print("Assistant Name:", name)
        print("\nSelected Instructions:", instructions)
        print("Run Instructions:", run_instructions)
    else:
        print("No instructions selected.")