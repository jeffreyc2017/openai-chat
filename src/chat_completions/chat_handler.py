from helpers.token_counter import num_tokens_from_messages
from openai_client_handler import get_openai_client
from function_call.function_call import function_call, tools
import traceback
from advanced_logging_setup import logger
from helpers.token_counts import TokenCounts
from openai.types.completion_usage import CompletionUsage

def format_user_input(user_input):
    """
    Formats the user input into a structured message for the OpenAI API.
    """
    return "\n".join(user_input)

def one_interaction(openai_client, model, messages, stream_enabled, ) -> tuple[str, any]:
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        stream=stream_enabled,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    print("\r-------------------------")  # Use carriage return to overwrite "AI is thinking..." message
    logger.debug(f'Response: {response}')
    print("AI: ", end="")

    response_content = ''
    usage = CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)

    if stream_enabled:
        for chunk in response:
            logger.debug(f'chunk: {chunk}')
            for choice in chunk.choices:
                if hasattr(choice, 'message') and choice.message is not None:
                    print(choice.message.content, end="")
                    response_content += choice.message.content
                elif hasattr(choice, 'delta'):
                    if choice.delta.content:
                        print(choice.delta.content, end="")
                        response_content += choice.delta.content
                    if choice.delta.tool_calls and choice.delta.role is not None:
                        second_response = function_call(model, messages, choice.delta)
                        print(second_response)
                        response_content = second_response.choices[0].message.content

                        # token_counts.update(second_response.usage.prompt_tokens, second_response.usage.completion_tokens, second_response.usage.total_tokens)
    else:
        for choice in response.choices:
            response_message = choice.message

            if response_message.tool_calls:
                second_response = function_call(model, messages, response_message)
                print(second_response.choices[0].message.content)
                response_content += second_response.choices[0].message.content
            else:
                print(response_message.content)
                response_content += response_message.content

    if hasattr(response, 'usage'):
        usage = response.usage
    return response_content, usage

def chat(system_prompt, model, stream_enabled=False, conversation_history=[]) -> tuple[bool, list]:
    """
    This function continuously accepts user input, breaks it into lines, and then sends it to
    OpenAI's chat completion API to generate a response based on the provided model.
    The conversation starts with the system initially stating the system_prompt only once.
    Warns the user if the number of tokens in a request exceeds 1000.
    """
    openai_client = get_openai_client()
    token_counts = TokenCounts()

    messages = []
    if conversation_history:
        messages = conversation_history
    else:
        messages.append({"role": "system", "content": system_prompt})

    print("--------------------------------")
    print("Enter your message. Press enter twice to send. Type 'exit' to quit.")

    while True:
        print("\nYou: ", end="")
        user_input = []
        while (line := input()) != "":
            if line.lower() == "exit":  # Allow the user to exit the chat
                print("Exiting chat. Goodbye!")
                token_counts.print()
                return False, messages
            elif line.lower() == "restart":
                return True, messages

            user_input.append(line)

        if not user_input:  # Skip empty messages
            continue

        message = format_user_input(user_input)
        messages.append({"role": "user", "content": message})

        logger.debug(f'Messages: {messages}')

        num_prompt_tokens = num_tokens_from_messages(messages, model)

        # Warn the user if the number of tokens for the current request exceeds 1000
        if num_prompt_tokens > 1000:
            print("Warning: Your request exceeds 1000 tokens, which may result in higher costs.")

        print("AI is thinking...", end="", flush=True)

        try:
            response_content, usage = one_interaction(
                openai_client=openai_client,
                model=model,
                messages=messages,
                stream_enabled=stream_enabled
            )
            if response_content:
                messages.append({"role": "assistant", "content": response_content})
            print("\n-------------------------")

            token_counts.update(usage.prompt_tokens, usage.completion_tokens, usage.total_tokens)
            token_counts.print()
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            traceback.print_exc()
            logger.error(traceback.format_exc())
            continue