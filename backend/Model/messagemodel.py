from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    author: User
    content: str
    created_at: datetime