import time
import sys
import random

def eliza_response(user_input):
    user_input = user_input.lower()

    # Rule 1: Simple keyword "mother", Can detect caps.
    if "mother" in user_input:
        return "Tell me more about your Mother please."

    # Rule 2: Simple Keyword "Father", Can detect caps
    if "father" in user_input:
        return "Tell me more about your father please."

    # Rule 3: Basic pattern "I am" / Custom responses
    if "i am" in user_input:
        response = user_input.split("i am", 1)[1].strip()
        return f"Why do you say you are {response}?"
    elif "im" in user_input:
        response = user_input.split("im", 1)[1].strip()
        return f"Why do you say you are {response}?"

    # Default fallback response
    return "Please, go on."


# Run a basic chat loop
def main():
    print("ELIZA: Hello, I am Eliza. What's on your mind?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "exit", "quit"]:
            print("ELIZA: Goodbye. Take care!")
            break
        response = eliza_response(user_input)
        print("ELIZA:", response)


if __name__ == "__main__":
    main()