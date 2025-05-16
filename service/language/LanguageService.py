import subprocess
import uuid
from typing import Dict

import ollama

from dependencies.PromptRepoDependency import get_prompt_repo
from dto.OllamaModel import Message, ChatResponse, Choice, SpeakerWeight
from eventHandler.LlmEvents import llmChatEvent


class LanguageService:
    def __init__(self):
        self.language = 'en'
        self.repo = get_prompt_repo()

    def set_language(self, language):
        self.language = language

    def get_language(self):
        return self.language

    def translate(self, text):
        # Placeholder for translation logic
        return f"Translated '{text}' to {self.language}"

    def build_prompt(self, messages: list[Message]) -> str:
        prompt = ""
        for msg in messages:
            role = msg.role.lower()
            if role == "system":
                prompt += f"[System]: {msg.content}\n"
            elif role == "user":
                prompt += f"[User]: {msg.content}\n"
            elif role == "assistant":
                prompt += f"[Assistant]: {msg.content}\n"
        prompt += "[Assistant]:"
        return prompt.strip()

    def chat(self, messages: list[Message], model: str, weights : Dict[str, SpeakerWeight]) -> dict:
        prompt_id = str(uuid.uuid4())
        self.repo.add_prompt(
            prompt_id=prompt_id,
            system_prompt=messages[0].content,
            user_prompt=messages[1].content
        )


        try:
            payload = {
                "system_prompt": messages[0].content,
                "user_prompt": messages[1].content,
                "model" : model,
                "prompt_id": prompt_id,
                "weights": weights
            }
            # llmChatEvent(dict(payload))
            llmChatEvent.apply_async(args=[payload], countdown=20)
        except Exception as e:
            print(f"Error occurred during LLM chat: {e}")

        return {
            "id": prompt_id,
            "object": "chat.completion",
            "status": "pending",
        }



