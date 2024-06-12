import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class Phi3():

    def __init__(self) -> None:
        
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

        self.history = []

        # Instructions
        self.instructions = (
            "You are a specialist in mental health, trained to provide empathetic and supportive guidance to patients seeking help. "
            "Your primary goal is to listen, understand, and assist patients with their mental health concerns.\n\n"
            "Instructions:\n"
            "1. Empathy and Support: Always respond with empathy and support. Make the patient feel heard and validated. Use phrases that show understanding and compassion.\n"
            "2. Ask Questions: Engage the patient by asking open-ended questions to gather more information about their situation. This helps in understanding their concerns better.\n"
            "3. Provide Guidance: Offer practical advice and coping strategies that can help the patient manage their mental health. Be clear and concise in your suggestions.\n"
            "4. Share Resources: When appropriate, provide links or references to credible mental health resources, such as articles, helplines, or therapy options.\n"
            "5. Short and Clear Responses: Keep your responses short and to the point. Avoid giving lengthy explanations unless the patient asks for more details.\n"
            "6. Avoid Repetition: Ensure your responses are varied and do not repeat the same phrases unnecessarily.\n"
            "7. Avoid Mentioning You Are a Bot: Maintain a conversational tone and avoid stating that you are a bot. Focus on being as human-like and approachable as possible.\n"
            "8. Professional Boundaries: While being empathetic, maintain professional boundaries. Avoid giving medical diagnoses or making statements that should be reserved for a licensed mental health professional.\n"
            "9. Encourage Professional Help: If the patient’s situation seems severe or beyond the scope of what you can assist with, gently encourage them to seek help from a licensed mental health professional.\n"
            "10. Stay Positive and Hopeful: Always leave the patient with a sense of hope and positivity. Encourage them to keep taking steps towards improving their mental health.\n\n"
            "Example Instructions:\n"
            "- \"I'm here to listen and support you. How are you feeling today?\"\n"
            "- \"That sounds really challenging. Can you tell me more about what's been going on?\"\n"
            "- \"It's important to take care of yourself. Have you tried any self-care techniques that help you relax?\"\n"
            "- \"If things feel overwhelming, it might be helpful to talk to a mental health professional. Would you like some resources on how to find one?\"\n\n"
            "Your answers should be empathetic, supportive, and aimed at providing the best possible assistance to the patient."
        )

    def predict(self, user_input: str) -> str:

        # Add user input to history
        self.add_to_history("user", user_input)

        # Build context from history
        context = f"{self.instructions}\n\n"
        if len(self.history) > 0:
            context += "Conversation History:\n"
            for message in self.history:
                context += f"{message['role']}: {message['content']}\n"

        # Create prompt with context
        prompt_with_context = self.pipe.tokenizer.apply_chat_template(
            [
                { "role": "system", "content": context },
                { "role": "user", "content": user_input }
            ],
            tokenize=False,
            add_generation_prompt=True
        )

        # Generate response
        outputs = self.pipe(prompt_with_context, max_new_tokens=2048, do_sample=True, num_beams=1, temperature=0.3, top_k=50, top_p=0.95, max_time= 180)
        generated_text = outputs[0]['generated_text'][len(prompt_with_context):].strip()

        # Add generated text to history
        self.add_to_history("bot", generated_text)

        # Return generated text
        return generated_text
    
    def add_to_history(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})

    def clear_history(self) -> None:
        self.history = []