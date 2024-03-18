from model_selector import choose_model
from prompt_creator import choose_prompt
from chat_handler import chat


def main():
    chat(system_prompt=choose_prompt(), model=choose_model())

if __name__ == "__main__":
    main()