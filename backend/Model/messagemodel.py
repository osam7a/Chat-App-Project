from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from backend.Model.usermodel import User

class Message(BaseModel):
    author: User
    content: str
    created_at: datetime
    meta: Optional[dict]