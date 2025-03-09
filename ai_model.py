from openai import OpenAI
from config.config import API_KEY
import json

client = OpenAI(api_key=API_KEY)


def create_calendar_event(event_params):
    """
    Stub function to create a calendar event.
    Replace this function with your actual Google Calendar API integration.
    """
    print(f"Creating calendar event with parameters: {event_params}")

def run_conversation(content):
    messages = [{"role": "user", "content": content}]
    tools = [
        {
        "type": "function",
        "function": {
            "name": "create_calendar_event",
            "description": "Create a calendar event based on the given parameters (like title, date, start time, and end time)",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the calendar event"
                    },
                    "date": {
                        "type": "string",
                        "description": "The date of the calendar event (format: 'YYYY-MM-DD')" 
                    },
                    "start_time": {
                        "type": "string",
                        "description": "The start time of the calendar event (format: 'HH:MM')" 
                    },
                    "end_time": {
                        "type": "string",
                        "description": "The end time of the calendar event (format: 'HH:MM')" 
                    }
                },
                "required": ["title", "date", "start_time", "end_time"],
                "additionalProperties": False
            },
            "strict": True
        },
    }]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        # messages.append(response_message)

        # available_functions = {
        #     "create_calendar_event": create_calendar_event,
        # }
        events = []
        for tool_call in tool_calls:
            try:
                event_params = json.loads(tool_call.function.arguments)
                events.append(event_params)
            except json.JSONDecodeError:
                print("Error parsing event parameters:", tool_call.function.arguments)
        
        if not events:
            print("No valid event details were parsed.")
            return
        
        # Build a confirmation message that lists each event's details.
        confirmation_text = "I parsed the following events:\n"
        for i, event in enumerate(events):
            confirmation_text += (
                f"Event {i+1}: Title: {event.get('title', 'N/A')}, "
                f"Date: {event.get('date', 'N/A')}, "
                f"Start Time: {event.get('start_time', 'N/A')}, "
                f"End Time: {event.get('end_time', 'N/A')}\n"
            )
        confirmation_text += "Do you want to create these events? (yes/no)"
        print(confirmation_text)
        # For this example, we use a console input for confirmation.
        # In your production code, you might send this message back to the chat interface.
        user_confirmation = input("Enter yes or no: ").strip().lower()
        if user_confirmation == "yes":
            for event in events:
                create_calendar_event(event)
            print("Events have been created.")
        else:
            print("Event creation cancelled.")
    else:
        print("No event details were parsed from the input.")

run_conversation("set up a team meeting from 10 to 1130 am on March 12th and March 13th")