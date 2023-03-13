# OpenAI Chatbot with gpt-3.5-turbo model

This is a simple chatbot that uses OpenAI's GPT-3.5-turbo language model to generate responses to user input.

## Installation
### Can be installed on most Linux terminal and also Termux on android
1. Clone the repository: `https://github.com/jacobhamilton12/chatgpt-on-terminal.git`
2. Install the required packages: `pip install -r requirements.txt`
> **Note:** This also works on termux on Android. If you have trouble installing dependencies on termux, read this https://github.com/termux/termux-packages/issues/13803

3. Set up an OpenAI API key by following the instructions [here](https://platform.openai.com/account/api-keys)
4. Add your API key as an environment variable `export OPENAI_KEY=<Your key here>`. Add this line to `$PREFIX/etc/bash.bashrc` to have it persist. Be sure to source after editing: `source $PREFIX/etc/bash.bashrc`

> **Note:** Do not include the greater than less than signs.

## Usage

To start the chatbot, run `main.py` using Python 3:

    python main.py

> **Note:** I've also added this as an alias to my bashrc `alias chat="python ~/chatgpt-on-terminal/main.py"`

The chatbot will prompt you to enter your input, and then it will generate a response using the GPT-3 model. The conversation history is stored in a list of dictionaries called `message_log`.

You can store system prompts in promptbook.json and select the prompt like so:
```python main.py "Default"```
replace Default with whatever key you made.

Format for promptbook.json
```
{
    "key": "prompt",
    "Default": "You are a helpful assistant",
    "Random": "Assistant is to respond to each prompt only with obscure incorrect facts"
}
```

To end the chatbot, type "q" at any time. Or ctrl+c

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* This chatbot was inspired by the [OpenAI GPT-3 Playground](https://beta.openai.com/playground/)
* The GPT-3 model is provided by [OpenAI](https://openai.com/)
