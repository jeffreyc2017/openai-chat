from model_selector import choose_model
from prompt_creator import choose_prompt
from chat_handler import chat


def main():
    model = choose_model()
    system_prompt = choose_prompt()
    chat(system_prompt=system_prompt, model=model)

if __name__ == "__main__":
    main()