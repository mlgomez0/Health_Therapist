from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Feedback(BaseModel):
    conversation_id: int
    user_score: Optional[int]
    user_feedback: Optional[str]