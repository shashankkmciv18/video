from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str  # system | user | assistant
    content: str

class ChatRequest(BaseModel):
    model: Optional[str] = "mistral"
    messages: List[Message]

class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    choices: List[Choice]
    usage: Optional[dict] = None
