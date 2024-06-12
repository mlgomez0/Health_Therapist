import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class Phi3():

    def __init__(self) -> None:
        pass
        # Settings
        model_name = 'acorreal/phi3-mental-health'
        adapter_name = 'acorreal/adapter-phi-3-mini-mental-health'
        compute_dtype = torch.bfloat16

        # Load model
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=compute_dtype)
        model = PeftModel.from_pretrained(model, adapter_name)
        model = model.merge_and_unload()
        model = model

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(adapter_name)

        self.pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    def predict(self, prompt: str) -> str:
        prompt = self.pipe.tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
        outputs = self.pipe(prompt, max_new_tokens=2048, do_sample=True, num_beams=1, temperature=0.3, top_k=50, top_p=0.95, max_time= 180)
        return outputs[0]['generated_text'][len(prompt):].strip()