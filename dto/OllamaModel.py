from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class Message(BaseModel):
    role: str  # system | user | assistant
    content : Any


class SpeakerWeight(BaseModel):
    name: str
    weight: str

class ChatRequest(BaseModel):
    model: Optional[str] = "mistral"
    messages: List[Message]
    weights: Optional[Dict[str, Dict[str, str]]] = None
    client_id : Optional[str] = None


class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    choices: List[Choice]
    usage: Optional[dict] = None
