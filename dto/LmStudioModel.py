from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: Optional[Any]  # Use `str` if it's always a string, else `Any` for JSON


class Choice(BaseModel):
    index: int
    logprobs: Optional[Any]
    finish_reason: Optional[str]
    message: Message


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class LLMResponseDTO(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
    stats: Optional[Dict[str, Any]] = {}
    system_fingerprint: Optional[str]
