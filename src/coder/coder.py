from helpers.model_selector import choose_model
from helpers.prompt_creator import choose_prompt
from chat_completions.chat_handler import one_interaction
from helpers.openai_client_handler import get_openai_client
from .setup_prompt import compose_first_prompt
from .extract_shell_script import extract_shell_script
from .scan_directory import scan_directory_and_prepare_prompt
import os

def setup_project(chat_completions_or_assistant, openai_client, model, streaming_enabled, instructions):
    messages = []
    messages.append({"role": "system", "content": instructions})
    prompt = compose_first_prompt('/home/cosmos/Documents/coder-test/project_description.yaml')
    messages.append({"role": "user", "content": prompt})
    if chat_completions_or_assistant == 'c':
        response, usage = one_interaction(
            openai_client=openai_client,
            model=model,
            messages=messages,
            stream_enabled=streaming_enabled
        )

        print(f'\nresponse: {response}')
        print(f'usage: {usage}')

        extract_shell_script(response_text=response)

def save_to_md_file(ai_response, project_directory):
    response_file_path = os.path.join(project_directory, 'ai_assistant_response.md')

    with open(response_file_path, 'w') as file:
        file.write(ai_response)

    print(f"AI assistant's response saved to: {response_file_path}")

def evolve_project(chat_completions_or_assistant, openai_client, model, streaming_enabled, instructions):
    messages = []
    messages.append({"role": "system", "content": instructions})
    project_root_directory = '/home/cosmos/Documents/coder-test/YellowCircleDrawer/'  # Update this path

    # Generate the comprehensive prompt for the AI
    prompt = scan_directory_and_prepare_prompt(project_root_directory)
    messages.append({"role": "user", "content": prompt})
    if chat_completions_or_assistant == 'c':
        response, usage = one_interaction(
            openai_client=openai_client,
            model=model,
            messages=messages,
            stream_enabled=streaming_enabled
        )

        print(f'\nresponse: {response}')
        print(f'usage: {usage}')
        save_to_md_file(response, project_directory=project_root_directory)

def engineer(chat_completions_or_assistant, model, streaming_enabled, instructions):
    openai_client = get_openai_client()
    # setup_project(
    #     chat_completions_or_assistant=chat_completions_or_assistant,
    #     openai_client=openai_client,
    #     model=model,
    #     streaming_enabled=streaming_enabled,
    #     instructions=instructions
    # )

    evolve_project(
        chat_completions_or_assistant=chat_completions_or_assistant,
        openai_client=openai_client,
        model=model,
        streaming_enabled=streaming_enabled,
        instructions=instructions
    )

if __name__ == "__main__":
    engineer(
        chat_completions_or_assistant='c',
        model='gpt-3.5-turbo',
        streaming_enabled=True,
        instructions='You are a senior software engineer.'
    )
