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

        # Instructions
        self.instructions = "\n".join([
            "You are an expert in mental health, trained to provide empathetic and supportive guidance to individuals seeking help.",
            "Your primary objective is to engage in meaningful conversations about mental health, asking insightful questions and offering thoughtful, compassionate responses.",
            "Avoid discussing or answering questions that are unrelated to mental health, such as topics about coding or other technical subjects.",
            "Always base your responses on the entire context of the conversation, ensuring you remember and reference all previous messages to provide continuity and relevance.",
            "Handle all user data with the utmost confidentiality and remind users to be cautious about sharing sensitive personal health information.",
            "Maintain a calm and supportive tone throughout all interactions, ensuring users feel heard and understood.",
            "Encourage users to express their thoughts and feelings openly, validate their experiences, and offer guidance or coping strategies when appropriate.",
            "If a user deviates from the topic of mental health, gently steer the conversation back to relevant topics to provide the most effective support."
        ])


    def predict(self, conversation_id: int, user_input: str) -> str:

        # Create context
        context = self.create_context(conversation_id)
        context.append({"role": "user", "content": user_input})

        print('_____________________________________________________________\n')
        print(context)
        print('_____________________________________________________________\n')

        # Create prompt with context
        prompt_with_context = self.pipe.tokenizer.apply_chat_template(context, tokenize=False)

        # Generate response
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

        # Remove the text after the word "Note:", "\n\n"
        generated_text = generated_text.split("Note:")[0].strip()
        generated_text = generated_text.split("\n\n")[0].strip()


        # Save conversation history
        self.db.create_message(conversation_id, user_input, generated_text)

        # Return generated text
        return generated_text
    
    def create_context(self, conversation_id: str) -> str:
        """
        Create the context for the conversation, including instructions and history.
        """
        
        # Get the messages from the conversation
        messages = self.db.get_messages(conversation_id)

        # Create an array with the messages splitting the user input and the bot output
        history = [ {"role": "assistant", "content": self.instructions} ]
        for message in messages:
            history.append({ "role": "user", "content": message['user_message'] })
            history.append({ "role": "assistant", "content": message['bot_response'] })
        return history

        # Create and return the context
        #context = "\n".join([f"{x['role']}: {x['content']}" for x in history])
        #return context
        
