from model_selector import choose_model
from prompt_creator import choose_prompt
from chat_handler import chat


def main():
    while True:
        model = choose_model()
        system_prompt = choose_prompt()
        if not chat(system_prompt=system_prompt, model=model):
            return

if __name__ == "__main__":
    main()