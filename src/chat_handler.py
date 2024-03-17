from prompt_creator import format_user_input
from token_counter import num_tokens_from_messages
from openai_client_handler import get_openai_client


def chat(system_prompt, model):
    """
    This function continuously accepts user input, breaks it into lines, and then sends it to
    OpenAI's chat completion API to generate a response based on the provided model.
    The conversation starts with the system initially stating the system_prompt only once.
    Warns the user if the number of tokens in a request exceeds 1000.
    """
    openai_client = get_openai_client()
    total_tokens = 0
    total_prompt_tokens = 0
    total_completion_tokens = 0

    print("--------------------------------")
    print("Enter your message. Press enter twice to send. Type 'exit' to quit.")

    while True:
        print("\nyou: ", end="")
        user_input = []
        while (line := input()) != "":
            if line.lower() == "exit":  # Allow the user to exit the chat
                print("Exiting chat. Goodbye!")
                print(f'Total tokens: {total_tokens}, total prompt tokens: {total_prompt_tokens}, total completion tokens: {total_completion_tokens}.')
                return
            user_input.append(line)

        if not user_input:  # Skip empty messages
            continue

        message = format_user_input(user_input)
        messages = []
        messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})

        num_prompt_tokens = num_tokens_from_messages(messages, model)
        
        # Warn the user if the number of tokens for the current request exceeds 1000
        if num_prompt_tokens > 1000:
            print("Warning: Your request exceeds 1000 tokens, which may result in higher costs.")

        print("AI is thinking...", end="", flush=True)

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_time",
                    "description": "Get the current time",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                        },
                        "required": ["location"],
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                }
            }
        ]

        stream = False
        
        try:
            response = openai_client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                stream=stream,
                temperature=1,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            print("\r")  # Use carriage return to overwrite "AI is thinking..." message
            print("-------------------------")
            print("AI: ", end="")

            print(response)
            if stream:
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        print(chunk.choices[0].delta.content, end="")

                total_prompt_tokens += num_prompt_tokens
            else:
                for choice in response.choices:
                    print(choice.message.content)

                total_prompt_tokens += response.usage.prompt_tokens
                total_completion_tokens += response.usage.completion_tokens
                total_tokens += response.usage.total_tokens
            
            print("-------------------------")
            print(f'Token count for this interaction: total tokens: {response.usage.total_tokens}, prompt tokens: {response.usage.prompt_tokens}, completion tokens: {response.usage.completion_tokens}.')
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            continue