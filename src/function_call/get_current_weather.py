import json

tool_get_current_weather = {
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

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(function_args):
    """Get the current weather in a given location"""
    
    location=function_args.get("location", "")
    unit=function_args.get("unit", "fahrenheit")
    
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

# def get_current_weather(location, unit="imperial"):
#     """
#     Get the current weather in a given location using the OpenWeatherMap API.
#     :param location: Name of the city, e.g., "Tokyo,JP"
#     :param unit: Temperature unit, "imperial" for Fahrenheit or "metric" for Celsius
#     """
# import requests
#     API_KEY = "your_openweathermap_api_key_here"
#     BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

#     # Constructing the complete URL
#     url = f"{BASE_URL}?q={location}&units={unit}&appid={API_KEY}"
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raises an HTTPError if the response was an error
#         data = response.json()
        
#         # Extracting required information
#         city = data['name']
#         temperature = data['main']['temp']
#         return json.dumps({"location": city, "temperature": str(temperature), "unit": "F" if unit == "imperial" else "C"})
    
#     except requests.RequestException as e:
#         print(f"Error fetching weather data: {e}")
#         return json.dumps({"location": location, "temperature": "unknown", "unit": unit})
