from openai_client_handler import get_openai_client
from .event_handler import EventHandler

class OpenAIAssistant:
    def __init__(self, name: str, instructions: str, model: str, streaming_enabled: bool = True):
        self._client = get_openai_client()
        self._name = name
        self._instructions = instructions
        self._model = model
        self._streaming_enabled = streaming_enabled
        self._assistant = None
        self._thread = None

        self._create_assistant()

    def _create_assistant(self):
        self._assistant = self._client.beta.assistants.create(
            name=self._name,
            instructions=self._instructions,
            tools=[{"type": "code_interpreter"}],
            model=self._model,
        )
        self._thread = self._client.beta.threads.create()

    def run(self, run_instructions: str, user_message: str):
        self._client.beta.threads.messages.create(
            thread_id=self._thread.id,
            role="user",
            content=user_message
        )

        if self._streaming_enabled:
            with self._client.beta.threads.runs.create_and_stream(
                thread_id=self._thread.id,
                assistant_id=self._assistant.id,
                instructions=run_instructions,
                event_handler=EventHandler(),
            ) as stream:
                stream.until_done()
        else:
            run = self._client.beta.threads.runs.create(
                thread_id=self._thread.id,
                assistant_id=self._assistant.id,
                instructions=run_instructions
            )

            import time

            while run.status in ['queued', 'in_progress', 'cancelling']:
                time.sleep(1)
                run = self._client.beta.threads.runs.retrieve(
                    thread_id=self._thread.id,
                    run_id=run.id
                )

            if run.status == 'completed':
                messages = self._client.beta.threads.messages.list(
                    thread_id=self._thread.id
                )
                self._print_sorted_messages(messages)
            else:
                print(run.status)

            print(run.usage)

    def _print_sorted_messages(self, messages):
        print("--------------------")
        sorted_messages = sorted(messages, key=lambda x: x.created_at)
        for message in sorted_messages:
            print(message.created_at, " ", message.role, ":")
            for content in message.content:
                print(content.text.value)
        print("--------------------")

if __name__ == "__main__":
    assistant = OpenAIAssistant(
        name="Math Tutor",
        instructions="You are a personal math tutor. Write and run code to answer math questions.",
        model="gpt-3.5-turbo",
        streaming_enabled=True
    )

    assistant.run(
        run_instructions="Please address the user as Jane Doe. The user has a premium account.",
        user_message="I need to solve the equation `3x + 11 = 14`. Can you help me?"
    )