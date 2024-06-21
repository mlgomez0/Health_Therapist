import os
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

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

    def start_chat(self, inputs, template):
        """
        Starts a chat with the language model using the provided inputs and template.
        
        Args:
            inputs (dict): A dictionary containing the input variables for the prompt.
            template (str): The template string for the prompt.
        
        Returns:
            str: The response from the language model.
        """
        # Create the prompt template
        prompt = PromptTemplate(
            input_variables=inputs.keys(),
            template=template
        )
        
        # Create the LLM instance
        llm = HuggingFaceHub(
            repo_id=self.model_name, 
            model_kwargs={"temperature": 1, "max_length": 1000}, 
            huggingfacehub_api_token=self.hf_api_token
        )

        # Create the chain
        chain = LLMChain(llm=llm, prompt=prompt)

        # Run the chain with the inputs
        response = chain.run(inputs)
        response = response.replace("\n", "")
        return response

