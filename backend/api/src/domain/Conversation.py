from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Conversation(BaseModel):
    id: int
    user_id: int
    model_name: str
    summary: Optional[str]
    timestamp: datetime
    user_score: Optional[int]
    user_feedback: Optional[str]