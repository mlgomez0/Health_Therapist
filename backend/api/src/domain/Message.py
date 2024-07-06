from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    user_input: str
    bot_output: str
    datetime: datetime