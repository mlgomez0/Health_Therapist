"""
This module contains the ResponseGenerator class, which is responsible for loading a language model,
training it with a dataset, and generating responses from input text.
"""

from dataset import dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class ResponseGenerator:
    """
    Class for generating responses using a language model.
    Attributes:
        model (AutoModelForCausalLM): Loaded language model.
        tokenizer (AutoTokenizer): Tokenizer corresponding to the model.
    """

    def __init__(self, model_name="distilgpt2"):
        """
        Initializes the ResponseGenerator class.

        Args:
            model_name (str, optional): Name of the model to load. Default is "distilgpt2".
        """

        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def train(self, dataset, epochs=10, lr=1e-5):
        """
        Trains the model with a dataset.

        Args:
            dataset (list): List of dictionaries with inputs and outputs.
            epochs (int, optional): Number of training epochs. Default is 10.
            lr (float, optional): Learning rate. Default is 1e-5.
        """

        dataset = [f"{example['input']} {self.tokenizer.sep_token} {example['output']}" for example in dataset]
        encodings = self.tokenizer(dataset, padding=True, truncation=True, return_tensors="pt")

        self.model.train()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)

        for epoch in range(epochs):
            for input_ids in encodings["input_ids"]:
                optimizer.zero_grad()
                outputs = self.model(input_ids, labels=input_ids)
                loss = outputs.loss
                loss.backward()
                optimizer.step()

    def generate_response(self, input_text, max_length=100, top_k=50, top_p=0.95, num_return_sequences=1):
        """
        Generates a response from input text.

        Args:
            input_text (str): Input text.
            max_length (int, optional): Maximum length of the generated response. Default is 100.
            top_k (int, optional): Number of most probable tokens to consider during generation. Default is 50.
            top_p (float, optional): Cumulative probability of tokens to consider during generation. Default is 0.95.
            num_return_sequences (int, optional): Number of sequences to generate. Default is 1.

        Returns:
            str: Generated response.
        """
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
        output_ids = self.model.generate(input_ids, max_length=max_length, do_sample=True, top_k=top_k, top_p=top_p, num_return_sequences=num_return_sequences)
        output_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return output_text
      
