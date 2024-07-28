from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    id: int
    conversation_id: int
    user_message: str
    bot_response: str
    timestamp: datetime
