from pydantic import BaseModel

class Request(BaseModel):
    text: str
    model: str
    conversation_id: str