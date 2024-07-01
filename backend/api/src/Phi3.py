import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from .infraestructure.ConversationRepository import ConversationRepository
from .infraestructure.DbContext import DbContext
from colorama import Fore, init

class Phi3():

    def __init__(self) -> None:

        print(Fore.MAGENTA + 'Initializing Phi3 model...')
        self.db = ConversationRepository(DbContext())
        
        # Settings
        model_name = 'acorreal/phi3-mental-health'
        adapter_name = 'acorreal/adapter-phi-3-mini-mental-health'
        compute_dtype = torch.bfloat16

        # Load model
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=compute_dtype)
        model = PeftModel.from_pretrained(model, adapter_name)
        model = model.merge_and_unload()
        print(Fore.MAGENTA + 'Model loaded')

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(adapter_name)
        print(Fore.MAGENTA + 'Tokenizer loaded')

        self.pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

        self.history = {}

        # Instructions
        self.instructions = "You are a specialist in mental health, trained to provide empathetic and supportive guidance to patients seeking help.",

    def predict(self, conversation_id: int, user_input: str) -> str:

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
            max_new_tokens=500,
            do_sample=True,
            num_beams=1,
            temperature=0.3,
            top_k=50,
            top_p=0.95,
            max_time= 600
        )
        generated_text = outputs[0]['generated_text'][len(prompt_with_context):].strip()

        # Remove the text after the word "(Note:"
        generated_text = generated_text.split("(Note:")[0].strip()

        # Add user input to history
        self.add_to_history(conversation_id, "user", user_input)

        # Add generated text to history
        self.add_to_history(conversation_id, "bot", generated_text)

        # Save conversation history
        self.db.create_message(conversation_id, user_input, generated_text)

        # Return generated text
        return generated_text
    
    def create_context(self, conversation_id: str) -> str:
        """
        Create the context for the conversation, including instructions and history.
        """

        history = self.history.get(conversation_id, [ {"role": "assistant", "content": self.instructions}, ])

        memory_context = "\n".join([f"{x['role']}: {x['content']}" for x in history])
        result = memory_context
        return result
        
    def add_to_history(self, conversation_id: str, role: str, content: str) -> None:
        self.history[conversation_id] = self.history.get(conversation_id, [])
        self.history[conversation_id].append({"role": role, "content": content})

    def clear_history(self, conversation_id) -> None:
        self.history[conversation_id] = []