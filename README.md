# OpenAI Chat

A Python script that interacts with the OpenAI API to generate conversational AI responses based on user input. It simulates a chat environment where the AI responds thoughtfully to each message.

## Features(to be implemented)

- Create prompt
- Select model
- Access website
- Read files
- Count tokens
- Calculate cost based on tokens and model

## Getting Started

This script leverages the OpenAI API to generate responses, creating an interactive chat experience. Follow these instructions to set up and run the script in your local environment.

## Prerequisites

- **Python 3:** Ensure Python 3.6 or newer is installed on your system. You can download it from [the official Python website](https://www.python.org/downloads/).
- **OpenAI API Key:** A valid OpenAI API key is required to authenticate requests. Obtain one by signing up at [OpenAI's API keys page](https://platform.openai.com/api-keys).
- **Configuration File:** The script requires a `config.cfg` file located in the same directory as the script itself. This file stores your API key and model preference. Create the file with the following content, replacing `YOUR_API_KEY` and `YOUR_MODEL` with your actual API key and model name:

```ini
[openai]
api_key = YOUR_API_KEY
model = YOUR_MODEL
```

## Installation

Before running the script, you need to install the OpenAI Python package. You can do this by running the following command in your terminal:

```bash
pip install openai
```

## Running the Script

To run the script, follow these steps:

1.	Open a terminal and navigate to the directory containing the script.
2.	Before using make, ensure you have a Makefile with appropriate commands for executing the script. If you’re not using a Makefile, you can directly run the script using Python:

    ```bash
    python openai_chat.py
    ```

3.	Upon running, you’ll be prompted to enter your message. Type your message and press enter. To send multiple lines, press enter after each line. When finished, press enter twice to send your message to the AI.
4.	The script will then process your input, displaying “AI is thinking…” while generating a response. Once completed, it will display the AI’s response.
5.	To exit the chat, type exit at the prompt.


Enjoy chatting with AI!