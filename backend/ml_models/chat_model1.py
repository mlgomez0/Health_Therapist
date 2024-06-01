from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class ChatModel1():
    
    def __init__(self):
        self.model_name = "t5-small"
        self.max_length = 2048
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

    def generate_response(self, input_text, max_length=150, min_length=30, length_penalty=2.0, num_beams=4):
        
        # Prepara el texto para el modelo
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt", max_length=max_length, truncation=True)

        # Genera el resumen
        summary_ids = self.model.generate(input_ids, max_length=self.max_length, min_length=min_length, length_penalty=length_penalty, num_beams=num_beams, early_stopping=True)

        # Decodifica y retorna el resumen
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary