"""
This module contains an example usage of the ResponseGenerator class to generate responses
from input text.
"""
# query.py

from first_model import ResponseGenerator

# Create an instance of the class
generator = ResponseGenerator()

# Generate a response
input_text = "I'm feeling lonely and without friends."
output_text = generator.generate_response(input_text)

print(f"Input: {input_text}")
print(f"Output: {output_text}")
