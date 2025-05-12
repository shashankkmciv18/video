import uuid


class PromptRepository:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def add_prompt(self, prompt_id, system_prompt, user_prompt, assistant_prompt: str = None):
        self.cursor.execute(
            "INSERT INTO prompts (id, system_prompt, user_prompt, assistant_prompt) VALUES (?,?, ?, ?)",
            (prompt_id, system_prompt, user_prompt, assistant_prompt)
        )
        self.conn.commit()

    def update_prompt(self, id, generated_response):
        self.cursor.execute(
            "UPDATE prompts SET generated_response = ?,WHERE id = ?",
            (generated_response, id)
        )

    def list_prompts(self):
        return list(self.prompts.keys())
