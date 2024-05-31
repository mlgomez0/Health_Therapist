from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class ChatModel1():
    
    def __init__(self, model_name="distilgpt2"):
        """
        Initializes the ResponseGenerator class.

        Args:
            model_name (str, optional): Name of the model to load. Default is "distilgpt2".
        """

        self.model_name = "distilbert-base-uncased-distilled-squad"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    def generate_response(self, input_text):
        context = "Transformers are very powerful models for NLP tasks."

        inputs = self.tokenizer.encode_plus(input_text, context, return_tensors="pt")
        outputs = self.model(**inputs)

        start_scores = outputs.start_logits
        end_scores = outputs.end_logits

        all_tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"].squeeze())
        answer = " ".join(all_tokens[torch.argmax(start_scores):torch.argmax(end_scores)+1])
        print(answer)