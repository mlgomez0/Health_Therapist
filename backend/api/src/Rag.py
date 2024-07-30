from .rag_modules.templates import PromptTemplate
from .rag_modules.azure_api_inference import LlmTalker
from .infraestructure.ConversationRepository import ConversationRepository
from .infraestructure.DbContext import DbContext


class Rag:
    """
    A class to perform retrieval-augmented generation (RAG) by generating responses based on user input and context.

    Methods
    -------
    predict(conversation_id: str, user_input: str) -> str:
        Generates a prediction/response based on the user input, context and chat history
    """
    def __init__(self) -> None:
        self.db = ConversationRepository(DbContext())

    def create_chat_history(self, conversation_id: str) -> str:
        """
        Create the chat history for the conversation, including instructions and history.
        """
        
        messages = self.db.get_messages(conversation_id)['messages']

        history = []
        for message in messages:
            history.append({ "role": "user", "content": message['user_message'] })
            history.append({ "role": "assistant", "content": message['bot_response'] })
        return history

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
        """

        chat_history = self.create_chat_history(conversation_id)
        context = PromptTemplate().one_shot(user_input)
        llm_talker = LlmTalker()

        answer = llm_talker.chat(chat_history, context, user_input)

        return answer
