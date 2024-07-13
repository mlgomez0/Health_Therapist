import os
from langchain.llms import HuggingFaceHub

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
            model_kwargs={"temperature": 1, "max_length": 1000}, 
            huggingfacehub_api_token=self.hf_api_token
        )
    
        return llm(prompt)

