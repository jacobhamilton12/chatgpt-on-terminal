import datetime
import openai
import os
import sys
import json

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
        max_tokens=4000-len(jstring),        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content

def log(message_log):
    now = datetime.datetime.now()
    nowstr = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("/data/data/com.termux/files/home/chatgpt-on-termux/log.txt", "a") as f:
        f.write(f"Chat ended: {nowstr}\n{str(message_log)}\n\n\n")

def get_prompt(key):
    # Open the JSON file
    with open('promptbook.json') as file:
        # Load the contents of the file into a dictionary
        data = json.load(file)
    
    # Get the prompt for the given key
    prompt = data[key]

    return prompt

# Main function that runs the chatbot
def main():
    key = "Default"
    if len(sys.argv) > 1:
        key = sys.argv[1]
        print(f"key: {key}")
    prompt = get_prompt(key)
    # Initialize the conversation history with a message from the chatbot
    message_log = [
        {"role": "system", "content": prompt}
    ]

    # Set a flag to keep track of whether this is the first request in the conversation
    first_request = True

    # Start a loop that runs until the user types "quit"
    while True:
        if first_request:
            # If this is the first request, get the user's input and add it to the conversation history
            user_input = input("You: ")
            message_log.append({"role": "user", "content": user_input})

            # Send the conversation history to the chatbot and get its response
            response = send_message(message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})
            print(f"AI assistant: {response}")

            # Set the flag to False so that this branch is not executed again
            first_request = False
        else:
            # If this is not the first request, get the user's input and add it to the conversation history
            user_input = input("You: ")

            # If the user types "quit", end the loop and print a goodbye message
            if user_input.lower() in ["quit", "q"]:
                print("Goodbye!")
                log(message_log)
                return

            message_log.append({"role": "user", "content": user_input})

            # Send the conversation history to the chatbot and get its response
            response = send_message(message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})
            print(f"AI assistant: {response}")


# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()
