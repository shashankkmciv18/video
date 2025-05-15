# script_repository.py
from typing import Union, List


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

    def create_dialogue(self, speaker, tone, dialogue, pause, seq_id, script_id, section_id,voice_id):
        self.cursor.execute(
            """INSERT INTO dialogues (speaker, tone, dialogue, pause, seq_id, script_id, section_id, voice_id)
               VALUES (?, ?, ?, ?, ?, ?, ?,?)""",
            (speaker, tone, dialogue, pause, seq_id, script_id, section_id, voice_id)
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

    def fetch_tts_op(self, batch_ids: list[str]):
        query = """
        SELECT
            dtm.status,
            d.seq_id,
            tj.result_url AS voice_url,
            d.pause AS pause_seconds
        FROM dialogue_tts_mapping dtm
        JOIN tts_jobs tj ON dtm.job_id = tj.job_id
        JOIN dialogues d ON dtm.dialogue_id = d.id
        WHERE dtm.batch_id IN ({seq})
        ORDER BY d.seq_id
        """.format(seq=','.join('?' for _ in batch_ids))

        return self.conn.execute(query, batch_ids).fetchall()



    def commit(self):
        self.conn.commit()
