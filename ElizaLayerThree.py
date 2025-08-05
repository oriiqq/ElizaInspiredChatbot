import json
import re
import random


class ElizaLayer3:
    """
    Implements Layer Three: A complex, script-driven ELIZA with ranking,
    substitutions, memory, and multiple reassembly rules.
    """

    def __init__(self, script_path):
        self.script = self._load_script(script_path)
        self.memory_stack = []
        # Keep track of the last used reassembly index for each decomp rule
        self.reassembly_counters = {}

    def _load_script(self, filepath):
        """Loads the JSON script file."""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading script file: {e}")
            return None

    def _substitute(self, text):
        """Performs pronoun substitutions on the input text."""
        words = text.lower().split()
        substituted_words = [self.script['substitutions'].get(word, word) for word in words]
        return ' '.join(substituted_words)

    def _get_response(self, user_input):
        """Generates a response based on the script's rules."""
        # 1. Find the highest-ranked keyword in the user input
        best_rule = None
        highest_rank = -1

        # Sort keywords by rank to ensure we check the most important ones first
        sorted_keywords = sorted(self.script['keywords'], key=lambda x: x['rank'], reverse=True)

        for keyword_data in sorted_keywords:
            keyword = keyword_data['key']
            if re.search(r'\b' + keyword + r'\b', user_input, re.IGNORECASE):
                # We found a keyword, now find a matching decomposition rule
                for rule in keyword_data['rules']:
                    match = re.search(rule['decomp'], user_input, re.IGNORECASE)
                    if match:
                        best_rule = rule
                        # If this rule triggers memory, store a follow-up
                        if keyword_data.get("memory"):
                            memory_responses = rule.get("memory_reassemb")
                            if memory_responses:
                                self.memory_stack.append(random.choice(memory_responses))
                        break
            if best_rule:
                break

        # 2. If a rule was found, generate a response from it
        if best_rule:
            # Get the reassembly options for this decomposition rule
            reassembly_options = best_rule['reassemb']
            decomp_pattern = best_rule['decomp']

            # Rotate through reassembly options to avoid repetition
            if decomp_pattern not in self.reassembly_counters:
                self.reassembly_counters[decomp_pattern] = 0

            counter = self.reassembly_counters[decomp_pattern]
            response = reassembly_options[counter % len(reassembly_options)]
            self.reassembly_counters[decomp_pattern] += 1

            # Apply substitutions and format the response
            match = re.search(best_rule['decomp'], user_input, re.IGNORECASE)
            if match and '{0}' in response:
                captured_text = match.group(1)
                substituted_capture = self._substitute(captured_text)
                return response.format(substituted_capture)
            return response

        # 3. If no rule matched, check the memory stack
        if self.memory_stack:
            return self.memory_stack.pop(0)

        # 4. If all else fails, use a generic fallback response
        return random.choice(self.script['fallback'])

    def chat(self):
        """Starts the main chat loop."""
        if not self.script:
            return

        print("Layer 3 ELIZA: Hello, I am ELIZA. How can I help you today?")
        print("(Type 'quit' to exit)")

        while True:
            user_input = input("> ")
            if user_input.lower() == "quit":
                print("Goodbye. It was a pleasure talking with you.")
                break

            response = self._get_response(user_input)
            print(response)


if __name__ == "__main__":
    eliza_bot = ElizaLayer3("doctor.json")
    eliza_bot.chat()