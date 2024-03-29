from typing_extensions import override
from openai import AssistantEventHandler
from openai.types.beta import AssistantStreamEvent
from openai.types.beta.threads import Text, TextDelta
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta, CodeInterpreterToolCall, RetrievalToolCall, FunctionToolCall
from openai.types.beta.threads.runs import RunStep, RunStepDelta
from advanced_logging_setup import logger
from function_call.function_call import available_functions
import json

class EventHandler(AssistantEventHandler):
    """
    How we want to handle the events in the response stream.

    References:
        - https://platform.openai.com/docs/assistants/overview?context=with-streaming
        - https://github.com/openai/openai-python/blob/main/helpers.md#assistant-events
    """
    last_function_response = None
    last_text = ''

    def __init__(self) -> None:
        super().__init__()
        self.last_function_response = []

    @override
    def on_event(self, event: AssistantStreamEvent) -> None:
        logger.debug(event.event)
        if event.event == "thread.run.step.created":
            details = event.data.step_details
            if details.type == "tool_calls":
                logger.debug("Generating code to interpret:\n\n```py")
        elif event.event == "thread.message.created":
            logger.debug("\nResponse:\n")

    @override
    def on_text_created(self, text: Text) -> None:
        print(f"\nassistant: ", end="", flush=True)

    @override
    def on_text_delta(self, delta: TextDelta, snapshot):
        print(delta.value, end="", flush=True)

    @override
    def on_text_done(self, text: Text) -> None:
        self.last_text = text.value

    def on_tool_call_created(self, tool_call: ToolCall):
        logger.debug(f'on_tool_call_created: {tool_call}')

    def on_tool_call_delta(self, delta: ToolCallDelta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                logger.debug(f'on_tool_call_delta: {delta}')

            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)
        else:
            logger.debug(f'on_tool_call_delta: {delta}')

            if delta.function.output:
                print(f"\n\noutput > {delta.function.output}")

    def on_tool_call_done(self, tool_call: CodeInterpreterToolCall | RetrievalToolCall | FunctionToolCall) -> None:
        logger.debug(f'on_tool_call_done: {tool_call}')
        if tool_call.type == 'function':
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(function_args)
            print(function_response)
            self.last_function_response.append(
                {
                    "tool_call_id": tool_call.id,
                    "output": function_response,
                }
            )
        return super().on_tool_call_done(tool_call)

    @override
    def on_run_step_done(self, run_step: RunStep) -> None:
        details = run_step.step_details
        if details.type == "tool_calls":
            for tool in details.tool_calls:
                if tool.type == "code_interpreter":
                    print("\n```\nExecuting code...")

    @override
    def on_run_step_delta(self, delta: RunStepDelta, snapshot: RunStep) -> None:
        details = delta.step_details
        if details is not None and details.type == "tool_calls":
            for tool in details.tool_calls or []:
                if tool.type == "code_interpreter" and tool.code_interpreter and tool.code_interpreter.input:
                    print(tool.code_interpreter.input, end="", flush=True)

    def on_exception(self, exception: Exception):
        logger.ERROR(f'error: {exception}')

    def on_end(self) -> None:
        logger.debug(f'on_end')
        return super().on_end()
