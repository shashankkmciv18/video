import subprocess
import uuid

from dto.ChatModel import Message, ChatResponse, Choice


class LanguageService:
    def __init__(self):
        self.language = 'en'

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

    def chat(self, messages: list[Message], model: str) -> dict:
        prompt = self.build_prompt(messages)

        try:
            result = subprocess.run(
                ["ollama", "run", model],
                input=prompt,
                capture_output=True,
                text=True,
                check=True
            )

            output = result.stdout.strip()

            response = ChatResponse(
                id=f"chatcmpl-{uuid.uuid4()}",
                choices=[
                    Choice(
                        index=0,
                        message=Message(role="assistant", content=output),
                        finish_reason="stop"
                    )
                ],
                usage=None
            )
            print(response)
            return response.dict()

        except subprocess.CalledProcessError as e:
            return {
                "error": f"Ollama execution failed: {e.stderr or str(e)}"
            }


