from pydantic import BaseModel

class LlmRequest(BaseModel):
    text: str
    model: str
    conversation_id: int
    user_id: int