# script_repository.py

class ScriptRepository:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def create_script(self, title):
        self.cursor.execute("INSERT INTO scripts (title) VALUES (?)", (title,))
        script_id = self.cursor.lastrowid
        self.commit()
        return script_id



    def create_section(self, name, script_id):
        self.cursor.execute(
            "INSERT INTO sections (name, script_id) VALUES (?, ?)",
            (name, script_id)
        )
        section_id = self.cursor.lastrowid
        self.commit()
        return section_id

    def create_dialogue(self, speaker, tone, dialogue, pause, seq_id, script_id, section_id):
        self.cursor.execute(
            """INSERT INTO dialogues (speaker, tone, dialogue, pause, seq_id, script_id, section_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (speaker, tone, dialogue, pause, seq_id, script_id, section_id)
        )
        self.commit()

    def get_dialogues_by_script_id(self, script_id):
        self.cursor.execute(
            "SELECT * FROM dialogues WHERE script_id = ? order by  seq_id",
            (script_id,)
        )
        return self.cursor.fetchall()

    def update_dialogue_job(self, dialogue_id, job_id, status):
        self.cursor.execute(
            "UPDATE dialogue_tts_mapping SET status = ? WHERE job_id = ? and dialogue_id = ?",
            (status, job_id, dialogue_id)
        )
        self.commit()

    def create_dialogue_mapping(self, dialogue_id, job_id, status, batch_id: str):
        self.cursor.execute(
            """
            INSERT INTO dialogue_tts_mapping (dialogue_id, job_id, status, batch_id)
            VALUES (?, ?, ?, ?)
            """,
            (dialogue_id, job_id, status, batch_id)
        )
        self.commit()

    def get_highest_batch_id(self):
        self.cursor.execute("SELECT MAX(batch_id) FROM dialogue_tts_mapping")
        result = self.cursor.fetchone()
        return result[0] if result else None

    def commit(self):
        self.conn.commit()
