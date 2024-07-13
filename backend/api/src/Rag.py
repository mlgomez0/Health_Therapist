import os
from .rag_modules.templates import PromptTemplate
from .rag_modules.hf_api_inference import LlmTalker


class Rag:
    """
    A class to perform retrieval-augmented generation (RAG) by generating responses based on user input and context.

    Methods
    -------
    predict(conversation_id: str, user_input: str) -> str:
        Generates a prediction/response based on the user input and context.
    """

    def predict(self, conversation_id: str, user_input: str) -> str:
        """
        Generates a prediction/response based on the user input and context.

        Parameters
        ----------
        conversation_id : str
            The ID of the conversation.
        user_input : str
            The input provided by the user.

        Returns
        -------
        str
            The generated response.

        Raises
        ------
        KeyError
            If the environment variable `PHI3_MODEL_NAME` is not set.
        """
        # Retrieve the model name from the environment variables
        phi_model_name = os.getenv("PHI3_MODEL_NAME")
        if not phi_model_name:
            raise KeyError("PHI3_MODEL_NAME environment variable is not set")

        # Prepare the query and context prompt
        query = user_input
        prompt_context = PromptTemplate().two_shot(query)

        # Initialize the LLM talker with the specified model
        llm_talker = LlmTalker(phi_model_name)

        # Generate the response with context
        answer_with_context = llm_talker.start_chat(prompt_context)

        # Extract and return the final answer
        answer = answer_with_context.split('<|assistant|>')[-1]
        return answer
