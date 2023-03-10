# OpenAI Chatbot with gpt-3.5-turbo model

This is a simple chatbot that uses OpenAI's GPT-3.5-turbo language model to generate responses to user input.

## Installation

1. Clone the repository: `https://github.com/jacobhamilton12/chatgpt-on-termux.git`
2. Install the required packages: `pip install -r requirements.txt`
> **Note:** If you have trouble installing dependencies on your termux, read this https://github.com/termux/termux-packages/issues/13803

3. Set up an OpenAI API key by following the instructions [here](https://platform.openai.com/account/api-keys)
4. Add your API key as an environment variable `export OPENAI_KEY=<Your key here>`. Add this line to `$PREFIX/etc/bash.bashrc` to have it persist. Be sure to source after editing: `source $P\
REFIX/etc/bash.bashrc`
> **Note:** Do not include the greater than less than signs.

## Usage

To start the chatbot, run `main.py` using Python 3:

    python main.py

> **Note:** I've also added this as an alias to my bashrc `alias chat="python ~/chatgpt-on-termux/main.py"`

The chatbot will prompt you to enter your input, and then it will generate a response using the GPT-3 model. The conversation history is stored in a list of dictionaries called `message_log`.

To end the chatbot, type "quit" at any time.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* This chatbot was inspired by the [OpenAI GPT-3 Playground](https://beta.openai.com/playground/)
* The GPT-3 model is provided by [OpenAI](https://openai.com/)
