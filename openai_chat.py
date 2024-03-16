from pathlib import Path
import configparser
from openai import OpenAI

from model_selector import choose_model
from prompt_creator import choose_prompt
from chat_handler import chat

# Initialization
config_file = Path.cwd() / "config.cfg"
config = configparser.ConfigParser()
config.read(config_file)

openai_client = OpenAI(api_key=config["openai"]["api_key"])

def main():
    model = choose_model()
    system_prompt = choose_prompt()
    chat(openai_client=openai_client, system_prompt=system_prompt, model=model)

if __name__ == "__main__":
    main()