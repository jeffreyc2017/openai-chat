from openai_client_handler import get_openai_client
import json

tools = [
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
        },
    }
]

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
# def get_current_weather(location, unit="fahrenheit"):
#     """Get the current weather in a given location"""
#     if "tokyo" in location.lower():
#         return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
#     elif "san francisco" in location.lower():
#         return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
#     elif "paris" in location.lower():
#         return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
#     else:
#         return json.dumps({"location": location, "temperature": "unknown"})

def get_current_weather(location, unit="imperial"):
    """
    Get the current weather in a given location using the OpenWeatherMap API.
    :param location: Name of the city, e.g., "Tokyo,JP"
    :param unit: Temperature unit, "imperial" for Fahrenheit or "metric" for Celsius
    """
    API_KEY = "your_openweathermap_api_key_here"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    # Constructing the complete URL
    url = f"{BASE_URL}?q={location}&units={unit}&appid={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response was an error
        data = response.json()
        
        # Extracting required information
        city = data['name']
        temperature = data['main']['temp']
        return json.dumps({"location": city, "temperature": str(temperature), "unit": "F" if unit == "imperial" else "C"})
    
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return json.dumps({"location": location, "temperature": "unknown", "unit": unit})

# Example usage
if __name__ == "__main__":
    print(get_current_weather("Tokyo,JP", unit="metric"))  # For temperature in Celsius

def function_call(model, messages, response_message):
    # Step 3: call the function
    # Note: the JSON response may not always be valid; be sure to handle errors
    available_functions = {
        "get_current_weather": get_current_weather,
    }  # only one function in this example, but you can have multiple
    messages.append(response_message)  # extend conversation with assistant's reply
    # Step 4: send the info for each function call and function response to the model
    tool_calls = response_message.tool_calls
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )
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
    # Step 1: send the conversation and available functions to the model
    messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}]
    
    response = get_openai_client().chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        return function_call(model, messages, response_message)

if __name__ == "__main__":
    response = run_conversation("gpt-3.5-turbo")
    print(response.choices[0].message.content)