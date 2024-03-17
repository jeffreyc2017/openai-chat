from model_selector import choose_model
from prompt_creator import choose_prompt
from chat_handler import chat
from website_content_analysis import compose_prompt


def main():
    model = choose_model()
    system_prompt = choose_prompt()
    print(f"Selected Prompt: {system_prompt}")

    if system_prompt:
        if isinstance(system_prompt, dict) and system_prompt.get("type") == "website_analysis":
            system_prompt = compose_prompt(system_prompt.get("url"))
            
        chat(system_prompt=system_prompt, model=model)
    else:
        print("No action taken.")

if __name__ == "__main__":
    main()