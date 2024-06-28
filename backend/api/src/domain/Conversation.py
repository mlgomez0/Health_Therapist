from pydantic import BaseModel
from Message import Message

class Conversation(BaseModel):
    text: str
    model: str
    conversation_id: str
    messages: list[Message]