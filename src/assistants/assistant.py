from openai_client_handler import get_openai_client
from .event_handler import EventHandler

_client = get_openai_client()
_assistant = None
_thread = None
_streaming = True

def create_assistant(name: str, instructions: str, model: str, streaming: bool = True):
    global _client
    global _assistant
    global _thread
    global _streaming
    
    _assistant = _client.beta.assistants.create(
        name=name,
        instructions=instructions,
        tools=[{"type": "code_interpreter"}],
        model=model,
    )

    _thread = _client.beta.threads.create()
    _streaming = streaming

def run():
    global _client
    global _thread
    global _assistant
    global _streaming

    message = _client.beta.threads.messages.create(
        thread_id=_thread.id,
        role="user",
        content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
    )

    run_instructions = "Please address the user as Jane Doe. The user has a premium account."

    if _streaming:
        with _client.beta.threads.runs.create_and_stream(
            thread_id=_thread.id,
            assistant_id=_assistant.id,
            instructions=run_instructions,
            event_handler=EventHandler(),
        ) as stream:
            stream.until_done()
    else:
        run = _client.beta.threads.runs.create(
            thread_id=_thread.id,
            assistant_id=_assistant.id,
            instructions=run_instructions
        )

        import time
    
        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1) # Wait for 1 second
            run = _client.beta.threads.runs.retrieve(
                thread_id=_thread.id,
                run_id=run.id
            )

        if run.status == 'completed': 
            messages = _client.beta.threads.messages.list(
                thread_id=_thread.id
            )
            print(messages.data)
            print("--------------------")
            for message in messages:
                print(message.created_at, " ", message.role, ":")
                for content in message.content:
                    print(content.text.value)
            print("--------------------")
            sorted_messages = sorted(messages, key=lambda x: x.created_at)
            for message in sorted_messages:
                print(message.created_at, " ", message.role, ":")
                for content in message.content:
                    print(content.text.value)
        else:
            print(run.status)

if __name__ == "__main__":
    create_assistant(
        name="Math Tutor",
        instructions="You are a personal math tutor. Write and run code to answer math questions.",
        model="gpt-3.5-turbo"
    )
    run()