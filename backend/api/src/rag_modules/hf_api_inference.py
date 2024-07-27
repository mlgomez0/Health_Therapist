import os
from langchain.llms import HuggingFaceHub
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

class LlmTalker:
    """
    A class to interact with a language model hosted on HuggingFaceHub.
    
    Attributes:
        model_name (str): The name of the model repository on HuggingFaceHub.
        hf_api_token (str): The API token for accessing HuggingFaceHub.
    """
    
    def __init__(self, model_name):
        """
        Initializes the LlmTalker with the specified model name.
        
        Args:
            model_name (str): The name of the model repository on HuggingFaceHub.
        """
        self.model_name = model_name
        self.hf_api_token = os.getenv("HF_API_TOKEN")
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        template = """<|system|>
                        You are a mental health therapist. Please provide a thoughtful and supportive response to the following user question, use the following history of the conversation as context
                        {chat_history}<|end|>
                        <|user|>
                        {input}<|end|>
                        <|assistant|>"""

        self.prompt = PromptTemplate(
            input_variables=["chat_history", "input"], template=template
        )

        self.model = HuggingFaceHub(
            repo_id=self.model_name, 
            model_kwargs={"temperature": 0.7, "max_length": 4000},
            huggingfacehub_api_token=self.hf_api_token
        )
        
        self.llm_chain = ConversationChain(
            llm=self.model,
            prompt=self.prompt,
            verbose=True,
            memory=self.memory
        )

    def start_chat(self, prompt):
        """
        Starts a chat with the language model using the provided inputs and template.
        
        Args:
            prompt (str): The complete prompt to.
        
        Returns:
            str: The response from the language model.
        """

        llm = HuggingFaceHub(
            repo_id=self.model_name, 
            model_kwargs={"temperature": 0.7, "max_length": 4000}, 
            huggingfacehub_api_token=self.hf_api_token
        )
    
        return llm(prompt)
    
    def start_chat_with_history(self, query):
    
        return self.llm_chain.predict(input=query)

