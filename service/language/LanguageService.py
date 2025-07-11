import json
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

    def chat(self, messages: list[Message], model: str, weights: Dict[str, SpeakerWeight], client_id: str) -> dict:
        prompt_id = str(uuid.uuid4())
        system_prompt = json.dumps(messages[0].content)
        user_prompt = json.dumps(messages[1].content)
        self.repo.add_prompt(
            prompt_id=prompt_id,
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        try:
            payload = {
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "model": model,
                "prompt_id": prompt_id,
                "weights": weights,
                "client_id": client_id
            }
            try:

                llmChatEvent.apply_async(args=[payload], countdown=20)
            except Exception as e:
                print(f"Exception: {e}")
        except Exception as e:
            print(f"Error occurred during LLM chat: {e}")

        return {
            "id": prompt_id,
            "object": "chat.completion",
            "status": "pending",
        }

