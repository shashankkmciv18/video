# script_repository.py

class ScriptRepository:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def create_script(self, title):
        self.cursor.execute("INSERT INTO scripts (title) VALUES (?)", (title,))
        script_id = self.cursor.lastrowid
        return script_id

    def create_section(self, name, script_id):
        self.cursor.execute(
            "INSERT INTO sections (name, script_id) VALUES (?, ?)",
            (name, script_id)
        )
        section_id = self.cursor.lastrowid
        return section_id

    def create_dialogue(self, speaker, tone, dialogue, pause, seq_id, script_id, section_id):
        self.cursor.execute(
            """INSERT INTO dialogues (speaker, tone, dialogue, pause, seq_id, script_id, section_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (speaker, tone, dialogue, pause, seq_id, script_id, section_id)
        )

    def commit(self):
        self.conn.commit()
