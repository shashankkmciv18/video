
class TtsRepository:
    def __init__(self, db_cursor, db_connection):
        self.cursor = db_cursor
        self.db = db_connection
        self.tts = None

    def set_tts(self, tts):
        self.tts = tts

    def get_tts(self):
        return self.tts

    def create_job_entry(self, text: str, voice_id: str, job_id: str, status: str, processor: str):
        # Insert a new TTS job into the database
        self.cursor.execute("""
            INSERT INTO tts_jobs (text, voice_id, job_id, status, processor)
            VALUES (?, ?, ?, ?, ?)
        """, (text, voice_id, job_id, status, processor))
        self.db.commit()

    def update_job(self, job_id: str, status: str, external_id: str, result_url: str = None):
        # Update a TTS job in the database
        self.cursor.execute("""
            UPDATE tts_jobs
            SET status = ?, external_id = ?, result_url = ?
            WHERE job_id = ?
        """, (status, external_id, result_url, job_id))
        self.db.commit()

    def get_job_status(self, job_id: str):
        # Retrieve the status of a TTS job from the database
        self.cursor.execute("""
            SELECT status FROM tts_jobs
            WHERE job_id = ?
        """, (job_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
