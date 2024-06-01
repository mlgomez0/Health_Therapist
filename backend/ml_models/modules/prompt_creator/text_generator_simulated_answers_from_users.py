"""
Loading a pre-trained language model to answer questions with inference or text
generation, where this pre-trained language model is used to generate new text
based on the input prompts or contexts.
"""

from transformers import pipeline
import random
from initial_prompts import initial_prompts  # Import the initial_prompts list

class TextGenerator:
    """
    A class to generate text responses based on input prompts (initial_prompts) using a pre-trained language model.
    
    Attributes:
        generator (pipeline): A Hugging Face Transformers pipeline object for text generation.
    
    Methods:
        generate_responses(prompts, num_responses=5, max_length=100):
            Generate text responses based on input prompts.
    """
    
    def __init__(self, model_name='gpt2'):
        """
        Initialize the TextGenerator instance.
        
        Args:
            model_name (str, optional): The name of the pre-trained language model to use for text generation.
                Defaults to 'gpt2'.
        """
        self.generator = pipeline('text-generation', model=model_name)
    
    def generate_responses(self, prompts, num_responses=5, max_length=100):
        """
        Generate text responses based on input prompts.
        
        Args:
            prompts (list): A list of prompts or contexts for which text responses need to be generated.
            num_responses (int, optional): The number of prompts to randomly select from the `prompts` list
                for generating responses. Defaults to 5.
            max_length (int, optional): The maximum length of the generated text responses. Defaults to 100.
        
        Returns:
            list: A list of generated text responses.
        """
        selected_prompts = random.sample(prompts, num_responses)
        responses = []
        for prompt in selected_prompts:
            response = self.generator(prompt, max_length=max_length, num_return_sequences=1)[0]['generated_text']
            responses.append(response)
        return responses

