from openai import OpenAI
from pathlib import Path
import configparser

_openai_client = None

def get_openai_client():
    global _openai_client
    if _openai_client is None:
        config_file = Path.cwd() / "config" / "config.cfg"
        config = configparser.ConfigParser()
        config.read(config_file)
        _openai_client = OpenAI(api_key=config["openai"]["api_key"])
    return _openai_client