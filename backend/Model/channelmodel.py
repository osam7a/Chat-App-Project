from typing import List, Optional
from pydantic import BaseModel, Field

from backend.Model.usermodel import User
from backend.Model.messagemodel import Message

class Channel(BaseModel):
    id: Optional[str] = Field(alias='_id')
    created_at: int
    name: str
    hash: str
    messages: List[Message]
    users: List[User]
    meta: Optional[dict]
