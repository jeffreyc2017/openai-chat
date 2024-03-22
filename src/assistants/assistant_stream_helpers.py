from typing_extensions import override
from openai import AssistantEventHandler
from openai.types.beta.threads import Text, TextDelta
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta
from openai.types.beta.threads.runs import RunStep, RunStepDelta
from advanced_logging_setup import logger

class EventHandler(AssistantEventHandler):
    """
    How we want to handle the events in the response stream.

    References:
        - https://platform.openai.com/docs/assistants/overview?context=with-streaming
        - https://github.com/openai/openai-python/blob/main/helpers.md#assistant-events
    """
    # @override
    # def on_event(self, event: AssistantStreamEvent) -> None:
    #     if event.event == "thread.run.step.created":
    #         details = event.data.step_details
    #         if details.type == "tool_calls":
    #             print("Generating code to interpret:\n\n```py")
    #     elif event.event == "thread.message.created":
    #         print("\nResponse:\n")

    @override
    def on_text_created(self, text: Text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta: TextDelta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call: ToolCall):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta: ToolCallDelta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)

            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)
        else:
            print("delta.type:", delta.type)
            logger.debug(f'delta: {delta}')

            if delta.function.output:
                print(f"\n\noutput > {delta.function.output}")

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
