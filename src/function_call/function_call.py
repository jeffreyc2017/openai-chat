"""
See https://platform.openai.com/docs/guides/function-calling
"""

import json
from openai_client_handler import get_openai_client
from function_call.get_current_date import get_current_date, tool_get_current_date
from function_call.get_current_weather import get_current_weather, tool_get_current_weather


tools = [
    tool_get_current_weather,
    tool_get_current_date,
]

available_functions = {
    "get_current_weather": get_current_weather,
    "get_current_date": get_current_date,
}

def function_call(model, messages, response_message):
    messages.append(response_message)  # extend conversation with assistant's reply
    tool_calls = response_message.tool_calls
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(function_args)
        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
    second_response = get_openai_client().chat.completions.create(
        model=model,
        messages=messages,
    )  # get a new response from the model where it can see the function response
    return second_response

def run_conversation(model):
    messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}]
    
    response = get_openai_client().chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        return function_call(model, messages, response_message)

if __name__ == "__main__":
    response = run_conversation("gpt-3.5-turbo")
    print(response.choices[0].message.content)

    print(get_current_weather("Tokyo,JP", unit="metric"))  # For temperature in Celsius

    print(get_current_date())