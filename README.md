# openai_chat

## Getting Started

This script uses the OpenAI API to generate AI responses to user input.

## Prerequisites

- You need to have python 3 installed.
- A valid API key for the OpenAI API. You can sign up for one at https://beta.openai.com/account/api-keys
- A config.cfg file in the same directory as the script. The file should contain the following:

```sh
[openai]
organization = YOUR_ORGANIZATION
api_key = YOUR_API_KEY
model = YOUR_MODEL
```

## Running the script

- Run the script by executing `make` and `make run` in your terminal
- You will be prompted to enter your message, please enter the message you would like to send
- The script will return the AI's response, and all the choices given by the OpenAI API

## Optimization

The code has been optimized to make use of the python's in-built libraries and avoid unnecessary loops and memory allocation.

## Note

The script uses os.environ["APP_CONFIG_FILE"] = os.getcwd() + "/config.cfg" to set the path for the config.cfg file. If you move the script to a different directory, please update the path accordingly.
