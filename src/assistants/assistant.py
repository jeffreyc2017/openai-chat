from openai_client_handler import get_openai_client
from .assistant_stream_helpers import EventHandler
from function_call.function_call import assistant_tools, assistant_function_call
import traceback
from advanced_logging_setup import logger
import time
from helpers.token_counts import TokenCounts

class OpenAIAssistant:
    def __init__(self, name: str, instructions: str, model: str, streaming_enabled: bool = True):
        self._client = get_openai_client()
        self._name = name
        self._instructions = instructions
        self._model = model
        self._streaming_enabled = streaming_enabled
        self._assistant = None
        self._thread = None
        self._token_counts = TokenCounts()

        self._create_assistant()

    def _create_assistant(self):
        self._assistant = self._client.beta.assistants.create(
            name=self._name,
            instructions=self._instructions,
            tools=assistant_tools,
            model=self._model,
        )
        self._thread = self._client.beta.threads.create()

    def remove(self):
        self._client.beta.assistants.delete(self._assistant.id)

    def run(self, run_instructions: str, user_message: str) -> str:
        self._client.beta.threads.messages.create(
            thread_id=self._thread.id,
            role="user",
            content=user_message
        )

        response = ''

        if self._streaming_enabled:
            event_handler = EventHandler()

            with self._client.beta.threads.runs.create_and_stream(
                thread_id=self._thread.id,
                assistant_id=self._assistant.id,
                instructions=run_instructions,
                event_handler=event_handler,
            ) as stream:
                stream.until_done()

            response += event_handler.last_text

            run = stream.current_run
            if run is not None:
                if event_handler.last_function_response is not None:
                    if run.status == 'requires_action':
                        with self._client.beta.threads.runs.submit_tool_outputs_stream(
                            run_id=run.id,
                            thread_id=self._thread.id,
                            tool_outputs=event_handler.last_function_response,
                            event_handler=EventHandler()
                        ) as stream:
                            stream.until_done()

                        response += event_handler.last_text
        else:
            run = self._client.beta.threads.runs.create(
                thread_id=self._thread.id,
                assistant_id=self._assistant.id,
                instructions=run_instructions
            )

            while not run.status == 'completed':
                logger.debug(f'run: {run}')
                if run.status == 'requires_action':
                    tool_outputs = assistant_function_call(run.required_action.submit_tool_outputs.tool_calls)
                    run = self._client.beta.threads.runs.submit_tool_outputs(
                        thread_id=self._thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )

                time.sleep(1)
                run = self._client.beta.threads.runs.retrieve(
                    thread_id=self._thread.id,
                    run_id=run.id
                )

            if run.status == 'completed':
                messages = self._client.beta.threads.messages.list(
                    thread_id=self._thread.id
                )

                logger.debug(f'messages: {messages}')

                message = messages.data[0]
                if message.role == 'assistant':
                    print("assistant:", end="")
                    for content in message.content:
                        print(content.text.value)
                        response += content.text.value
            else:
                print(run.status)

            '''
            "usage": {
                "prompt_tokens": 123,
                "completion_tokens": 456,
                "total_tokens": 579
            }
            '''
            self._token_counts.update(run.usage.prompt_tokens, run.usage.completion_tokens, run.usage.total_tokens)

        return response

    def _print_sorted_messages(self, messages):
        print("--------------------")
        sorted_messages = sorted(messages, key=lambda x: x.created_at)
        for message in sorted_messages:
            if message.role == 'assistant':
                print("assistant:", end="")
                for content in message.content:
                    print(content.text.value)
        print("--------------------")

def chat(name, instructions, run_instructions, model, streaming_enabled=True, conversation_history=[]) -> tuple[bool, list]:
    from chat_completions.chat_handler import format_user_input

    try:
        assistant = OpenAIAssistant(
            name=name,
            instructions=instructions,
            model=model,
            streaming_enabled=streaming_enabled
        )

        messages = []
        if conversation_history:
            messages = conversation_history

        while True:
            print("\nYou: ", end="")
            user_input = []
            while (line := input()) != "":
                if line.lower() == "exit":  # Allow the user to exit the chat
                    print("Exiting chat. Goodbye!")
                    return False, messages
                elif line.lower() == "restart":
                    return True, messages

                user_input.append(line)

                if not user_input:  # Skip empty messages
                    continue

                message = format_user_input(user_input)
                response = assistant.run(
                    run_instructions=run_instructions,
                    user_message=message
                )

                messages.append({"role": "user", "content": message})
                messages.append({"role": "assistant", "content": response})
    except Exception as e:
        print(f'error: {e}')
        logger.error(traceback.format_exc())
        print('restart...')
        return True, messages

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