from db import getDB

class LlmClientRepository:
    def __init__(self):
        self.cursor, self.conn = getDB()

    def get_client_by_id(self, client_id):
        """
        Fetch a client by their ID from the clients table
        
        Args:
            client_id: The ID of the client to fetch
            
        Returns:
            dict: Client data as a dictionary if found, None otherwise
        """
        self.cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        result = self.cursor.fetchone()
        if result:
            # Return a dict mapping column names to values
            return dict(result)
        return None
