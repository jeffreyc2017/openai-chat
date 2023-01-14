import os
import openai
import configparser

# Initialization
# This code initiates the configuration file that stores all the credentials from OpenAI and then reads the values from the configuration file using configparser. The organization and API key are then stored in the openai module and the model name is stored in the model variable.
config_file = os.getcwd() + "/config.cfg"
os.environ["APP_CONFIG_FILE"] = config_file
config = configparser.ConfigParser()
config.read(config_file)

openai.organization = config["openai"]["organization"]
openai.api_key = config["openai"]["api_key"]
model = config["openai"]["model"]


# This function is responsible for accepting user input, breaking it up into lines, and then constructing the final message with \n between the lines. It then passes the message to OpenAI's Completion.create method to generate the AI response. Finally, it prints out all the choices given by OpenAI.
def chat():
    while True:
        print("you: ", end="")

        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)

        text = "\n".join([line for line in lines])

        print("AI: ", end="")
        response = openai.Completion.create(
            model=model,
            prompt=text,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            echo=False,
        )

        for choice in response.choices:
            print(choice.text)


chat()
