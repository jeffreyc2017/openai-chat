# OpenAI Chat

A Python script that interacts with the OpenAI API to generate conversational AI responses based on user input. It simulates a chat environment where the AI responds thoughtfully to each message.

## Features

- [x] Create prompt :tada:
- [x] Select model :tada:
- [x] Function call

  - Chat completions mode

    - [x] Streaming
    - [x] Without streaming

  - Assistant mode

    - [x] Streaming
    - [x] Without streaming

  - [x] Access website :tada:

    This is a function call.

    Usage:

    You: Check the content of the webpage: example.com (this will parse the html text within the page)

    You: Check the full content of the webpage: example.com (this will grad all the content including the js)

  - [x] Get current date and time :tada:

    A function call to get the time and date based on the time zone.

  - [ ] Get current weather

    A function call to get the current weather based on the location.
    Currently it's a dummy function. Fully implementation needs to register a weather API to fetch the weather data.

  - [ ] Read files

    A function call.

- [x] Count tokens :tada:

    Utilizes `tiktoken` for accurate token counting, enabling estimation of the number of tokens used by prompts and responses. This is vital for effectively managing API costs, especially given the diverse pricing models based on token usage.

- [x] Calculate cost based on tokens and model :tada:

    See [OpenAI API pricing](https://openai.com/pricing) for more details.

## Getting Started

This script leverages the OpenAI API to generate responses, creating an interactive chat experience. Follow these instructions to set up and run the script in your local environment.

## Prerequisites

- **Python 3:** Ensure Python 3.6 or newer is installed on your system. Download it from [the official Python website](https://www.python.org/downloads/).
- **OpenAI API Key:** A valid OpenAI API key is required for authentication. Obtain one by signing up at [OpenAI's API keys page](https://platform.openai.com/api-keys).
- **Configuration File:** A `config.cfg` file in the same directory as the script is needed. This file stores your API key. Replace `YOUR_API_KEY` with your actual API key:

```ini
[openai]
api_key = YOUR_API_KEY
```

## Installation

Before running the script, you need to install the OpenAI Python package. You can do this by running the following command in your terminal:

```bash
pip install -r requirements.txt
```

or

```bash
make
```

## Running the Script

To run the script, follow these steps:

1. Open a terminal and navigate to the directory containing the script.
2. Before using make, ensure you have a Makefile with appropriate commands for executing the script. If you’re not using a Makefile, you can directly run the script using Python:

    ```bash
    python src/main.py
    ```

    or

    ```bash
    make run
    ```

3. Upon running, you’ll be prompted to enter your message. Type your message and press enter. To send multiple lines, press enter after each line. When finished, press enter twice to send your message to the AI.
4. The script will then process your input, displaying “AI is thinking…” while generating a response. Once completed, it will display the AI’s response.
5. To exit the chat, type exit at the prompt.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Author

- **Jeffrey Cai** - *Initial work* - [jeffreyc2017](https://github.com/jeffreyc2017)

## Acknowledgments

- Hat tip to anyone whose code was used

Enjoy chatting with AI!
