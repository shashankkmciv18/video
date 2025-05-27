class InstagramRepository:
    def __init__(self, db_cursor, db_connection):
        self.cursor = db_cursor
        self.db = db_connection

    def create_creation_entry(self, instagram_creation_id: int, is_published: bool):
        # Insert Instagram upload data into the database
        self.cursor.execute("""
            INSERT INTO instagram_uploads (instagram_creation_id, is_published)
            VALUES (?, ?)
        """, (instagram_creation_id, is_published))
        self.db.commit()

    def update_creation_entry(self, instagram_creation_id: str, is_published: bool, instagram_content_id: str):
        # Retrieve a single Instagram upload record by ID
        # Execute the update query
        self.cursor.execute("""
            UPDATE instagram_uploads
            SET instagram_content_id = ?, is_published = ?
            WHERE instagram_creation_id = ?;
        """, (instagram_content_id, is_published, instagram_creation_id))
        self.db.commit()
