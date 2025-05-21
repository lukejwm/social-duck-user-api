from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StartChatRequest(BaseModel):
    business_email: str
    user_email: str
    message: str

class SendMessageRequest(BaseModel):
    session_id: str
    message: str
    sender: str
    receiver: str

class ChatHistory(BaseModel):
    session_id: str
    business_id: int
    business_email: str
    user_id: int
    user_email: str
    message: str
    sender: str
    receiver: str
    timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True
