from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import json

tool_get_current_date = {
    "type": "function",
    "function": {
        "name": "get_current_date",
        "description": "Get the current date and time",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The time zone info, e.g. UK/London",
                },
            },
        },
    },
}

def get_current_date(function_args):
    location=function_args.get("location", None)
    
    if location:
        # Get the current UTC date and time
        datetime_utc = datetime.now(timezone.utc)
        
        # Convert the UTC datetime to the desired location's time
        datetime_location = datetime_utc.astimezone(ZoneInfo(location))
        
        return json.dumps({"datetime": datetime_location.isoformat(), "location": location})
    else:
        return json.dumps({"datetime": datetime.now().isoformat()})

if __name__ == "__main__":
    print(get_current_date({"location": "America/New_York"}))
    print(get_current_date({"location": "Europe/London"}))
    print(get_current_date({}))