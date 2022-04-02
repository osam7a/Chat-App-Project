from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    ID: int
    username: str
    password: str
    meta: Optional[dict]