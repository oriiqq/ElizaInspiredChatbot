import re
import random
import json

def load_rules():
    with open('package.json', 'r') as f:
        rules = json.load(f)
    return rules["rules"]

def load_fallback():
    with open('package.json', 'r') as f:
        fallback = json.load(f)
    return fallback["fallback"]


def eliza_response(user_input, rules, fallback):
    for rule in rules:
        match = re.match(rule["pattern"], user_input, re.IGNORECASE)
        if match:
            response_template = random.choice(rule["responses"])
            groups = match.groups()
            return response_template.format(*groups)
    return fallback


def main():
    print("ELIZA: Hello. How are you feeling today?")
    rules = load_rules()
    fallback = load_fallback()

    while True:
        user_input = input("> ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("ELIZA: Goodbye, Take care!")
            break
        reply = eliza_response(user_input, rules, fallback)
        print("ELIZA: ", reply)

if __name__ == "__main__":
    main()
