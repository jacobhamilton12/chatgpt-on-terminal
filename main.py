import datetime
import openai
import os
import sys
import json
import signal

# Get the value of an environment variable
openai.api_key = os.environ.get('OPENAI_KEY')

MAX_TOKENS = 4000
MIN_TOKENS = 1000

# Function to send a message to the OpenAI chatbot model and return its response
def send_message(message_log):
    jstring = json.dumps(message_log)
    while MAX_TOKENS - len(jstring) < MIN_TOKENS:
        # don't pop first which is the system prompt
        message_log.pop(1)
        jstring = json.dumps(message_log)
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=MAX_TOKENS-len(jstring),        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content

def exit_log():
    now = datetime.datetime.now()
    nowstr = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("~/chatgpt-on-termux/log.txt", "a") as f:
        f.write(f"Chat ended: {nowstr}\n{str(message_log)}\n\n\n")

def get_system_prompt(key):
    if not os.path.exists('promptbook.json'):
        return "You are a helpful assistant"
    # Open the JSON file
    with open('promptbook.json') as file:
        # Load the contents of the file into a dictionary
        data = json.load(file)
    
    # Get the prompt for the given key
    prompt = data[key]

    return prompt

def signal_handler(sig, frame):
    print('sigint detected')
    exit_log()
    exit(0)

def read_multiline_string(esc):
    print(f"You (esc={esc}): ", end="")
    lines = []
    while True:
        line = input()
        if line == esc:
            break
        lines.append(line)
    multiline_string = '\n'.join(lines)
    return multiline_string

def read_normal():
    return input("You: ")

# Main function that runs the chatbot
def main():
    global message_log
    mode = input("Multiline mode? y/n ")
    reader = read_normal
    if mode == "y":
        esc = input("Enter escape sequence: ")
        print(f"Enter {esc} on an empty line to end a sequence, enter by itself to end chat")
        reader = lambda: read_multiline_string(esc)
    else:
        print("Enter q to exit")
        
    # Start a loop that runs until the user types "quit"
    while True:
        user_input = reader()

        # If the user types "quit", end the loop and print a goodbye message
        if user_input.lower() in ["quit", "q", ""]:
            print("Goodbye!")
            exit_log()
            return

        message_log.append({"role": "user", "content": user_input})

        # Send the conversation history to the chatbot and get its response
        response = send_message(message_log)

        # Add the chatbot's response to the conversation history and print it to the console
        message_log.append({"role": "assistant", "content": response})
        print(f"AI assistant: {response}")

signal.signal(signal.SIGINT, signal_handler)

key = "Default"
if len(sys.argv) > 1:
    key = sys.argv[1]
    print(f"key: {key}")
prompt = get_system_prompt(key)

# Initialize the conversation history with a message from the chatbot                                
message_log = [                                          {"role": "system", "content": prompt}            ]

# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()
