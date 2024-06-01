"""
This script shows how to use the TextGenerator class to generate text responses
based on input prompts and print the generated responses.
"""

from text_generator_simulated_answers_from_users import TextGenerator
from initial_prompts import initial_prompts

# Create an instance of the TextGenerator class
text_generator = TextGenerator()

# Generate responses based on the initial_prompts list
responses = text_generator.generate_responses(initial_prompts)

# Print the generated responses
for i, response in enumerate(responses):
    print(f"## Response {i+1}")
    print(response)
    print()
