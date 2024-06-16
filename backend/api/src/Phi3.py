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

        self.history = {}

        # Instructions
        self.instructions = (
            "Instructions: \n"
            "You are a specialist in mental health, trained to provide empathetic and supportive guidance to patients seeking help.",
            'Use the context of the conversation to provide the best possible response to the user, even remembering previous interactions.',
            'Avoid provide meta-responses, such as "I am a chatbot" or "I am a computer program" or "The chatbot\'s memory of this conversation would include the user\'s name".',
            "Be specific, do not write thinhs the user did not aks for.",
        )

    def predict(self, conversation_id: str, user_input: str) -> str:

        # Create context
        context = self.create_context(conversation_id)

        # Create prompt with context
        prompt_with_context = self.pipe.tokenizer.apply_chat_template(
            [
                {"role": "assistant", "content": context},
                {"role": "user", "content": user_input}
            ],
            tokenize=False
        )

        # Generate response
        print('\n--------------------\nConversation_id:', conversation_id, '\nPrompt:\n', prompt_with_context, '\n--------------------\n')
        outputs = self.pipe(
            prompt_with_context,
            max_new_tokens=384,
            do_sample=True,
            num_beams=1,
            temperature=0.3,
            top_k=50,
            top_p=0.95,
            max_time= 180
        )
        generated_text = outputs[0]['generated_text'][len(prompt_with_context):].strip()

        # Add user input to history
        self.add_to_history(conversation_id, "user", user_input)

        # Add generated text to history
        self.add_to_history(conversation_id, "bot", generated_text)

        # Return generated text
        return generated_text
    
    def create_context(self, conversation_id: str) -> str:
        """
        Create the context for the conversation, including instructions and history.
        """

        history = self.history.get(conversation_id, [])
        memory_context = "\n".join([f"{x['role']}: {x['content']}" for x in history])
        result = f"The following is a conversation with you. The chatbot has the following memories of this conversation:\n{memory_context}\n"
        return result
        
    def add_to_history(self, conversation_id: str, role: str, content: str) -> None:
        self.history[conversation_id] = self.history.get(conversation_id, [])
        self.history[conversation_id].append({"role": role, "content": content})

    def clear_history(self, conversation_id) -> None:
        self.history[conversation_id] = []