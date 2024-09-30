# https://www.youtube.com/shorts/wPa9_fd9-dk
from pocketgroq import GroqProvider
import os
import sys
from datetime import datetime as dt
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Access environment variables
groq_api_key = os.getenv('GROQ_API_KEY')

'''
Please share the details about the type of agent you have in mind, such as:

1. Industry or sector (e.g., sales, customer support, healthcare, finance)
2. Job title or role (e.g., manager, consultant, analyst, expert)
3. Personality traits (e.g., friendly, assertive, empathetic, formal)
4. Tone and language (e.g., professional, conversational, technical, humorous)
5. Any specific characteristics or attributes you'd like me to embody

The more information you provide, the better I'll be able to understand and mimic the agent you have in mind.
[2024-09-13 09:29:07]  user : I need assistance in the following ways with the code that I am about to paste after my requests.  1) I would like to be able to pass Groq information about the expected role of the Agent that I would like to work with 1) receive some sort of agent id back from from groq so that the conversation we are having will be known to that agent as I expect to have multiple exchanges with each agent and would like the agent to remember earlier information shared with it.  Here is a pasting of the python code... from pocketgroq import GroqProvider
[2024-09-13 09:29:08]  groq : I can help you with that. It seems like you want to pass some information about the expected role of the Agent to Groq and also receive an agent ID back from Groq so that the conversation can be tracked. Here's how you can modify your code to achieve this:

```
from pocketgroq import GroqProvider

# Initialize Groq provider
groq_provider = GroqProvider('your_groq_url')

# Define the expected role of the Agent
expected_role = 'your_expected_role'

# Create a new conversation with Groq
conversation = groq_provider.create_conversation()

# Set the expected role of the Agent in the conversation
conversation.set_agent_role(expected_role)

# Get the agent ID from the conversation
agent_id = conversation.get_agent_id()

print(f"Agent ID: {agent_id}")
```

In this code, we first initialize the Groq provider with your Groq URL. Then, we define the expected role of the Agent. We create a new conversation with Groq using the `create_conversation` method, and then set the expected role of the Agent in the conversation using the `set_agent_role` method. Finally, we get the agent ID from the conversation using the `get_agent_id` method and print it out.

This way, you can pass the expected role of the Agent to Groq and receive an agent ID back, which can be used to track the conversation and remember earlier information shared with the agent.

Please replace `'your_groq_url'` and `'your_expected_role'` with your actual Groq URL and expected role.
'''


def clearscreen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')


def log_it(who, msg):
    log_file = f'groq_logs/{dt.now().strftime('%Y-%m-%d')}_conversation_log.txt'
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write('')  # Create an empty file
            f.close()
    with open(log_file, 'a') as f:
        timestamp = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'[{timestamp}] {who:>5} : {msg}\n')


def main():
    # Initialize the GroqProvider
    groq = GroqProvider(api_key=groq_api_key)
#    clearscreen()
    print("Welcome to the Simple Groq AI Chat!")
    print("Type 'exit' to end the conversation.")

    # Start the chat loop
    while True:
        # Get user input
        user_input = input("You: ").strip()
        log_it('user', user_input)

        # Check if the user wants to exit
        if user_input.lower() == 'exit':
            msg = 'Goodbye!'
            log_it('groq', msg)
            print(msg)
            sys.exit(0)

        try:
            # Generate a response using Groq
            response = groq.generate(user_input)
            log_it('groq', response)
            clearscreen()
            print("AI:", response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        print('')
        print('')

if __name__ == "__main__":
    main()



