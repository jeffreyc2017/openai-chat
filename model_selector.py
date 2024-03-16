def list_models():
    """
    Returns a list of available models.
    This function can be expanded to dynamically fetch models from an API.
    https://platform.openai.com/docs/models/continuous-model-upgrades
    """
    return [
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-instruct",
        "gpt-4",
        "gpt-4-32k",
        "gpt-4-turbo-preview",
        # Add more models as needed
    ]

def choose_model():
    """
    Allows the user to select a model from the available list.
    """
    models = list_models()
    print("Available models:")
    for i, model in enumerate(models, start=1):
        print(f"{i}. {model}")
    print("Select a number to choose a model:")

    while True:
        choice = input()
        try:
            chosen_index = int(choice) - 1
            if chosen_index in range(len(models)):
                return models[chosen_index]
            else:
                raise ValueError
        except ValueError:
            print("Invalid choice. Please enter a number from the list.")
