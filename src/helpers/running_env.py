from helpers.model_selector import choose_model
from helpers.prompt_creator import choose_prompt

class RunningEnv:
    chat_completions_or_assistant: str
    model: str
    streaming_enabled: bool
    category_name: str
    instructions: str
    run_instructions: str

    def __init__(
        self,
        chat_completions_or_assistant='',
        model='gpt-3.5-turbo',
        streaming_enabled=False,
        category_name='',
        instructions='',
        run_instructions=''
    ) -> None:
        self.chat_completions_or_assistant = chat_completions_or_assistant
        self.model = model
        self.streaming_enabled = streaming_enabled
        self.category_name = category_name
        self.instructions = instructions
        self.run_instructions = run_instructions

def setup_env() -> RunningEnv:
    chat_completions_or_assistant = input("Chat completions(C/c) or Assistant(A/a)?:").lower()
    if chat_completions_or_assistant != 'a' and chat_completions_or_assistant != 'c':
        return None
    streaming_enabled_input = input("Enable streaming?(Y/n):").lower()
    streaming_enabled = (streaming_enabled_input == 'y') or (not streaming_enabled_input)
    model = choose_model()

    # Unpack returned values from choose_prompt
    category_name, instructions, run_instructions = choose_prompt()

    # Check if any value is None to determine if we should exit
    if instructions is None or category_name is None or run_instructions is None:
        print("Exiting the application.")
        return None

    return RunningEnv(
        chat_completions_or_assistant=chat_completions_or_assistant,
        model=model,
        streaming_enabled=streaming_enabled,
        category_name=category_name,
        instructions=instructions,
        run_instructions=run_instructions
    )
