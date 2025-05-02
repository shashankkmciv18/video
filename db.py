import sqlite3
import os
from contextlib import contextmanager

_db_connection = None
_db_cursor = None


def get_db_1():
    global _db_connection, _db_cursor
    if _db_connection is None or _db_cursor is None:
        _db_connection = sqlite3.connect("database.db", check_same_thread=False)
        _db_cursor = _db_connection.cursor()
    return _db_cursor, _db_connection

@contextmanager
def get_db():
    db_path = os.path.join(os.path.dirname(__file__), "database.db")
    print(f"Connecting to database at {db_path}")

    conn = sqlite3.connect(db_path)
    print("Database connection established.")

    # Optional: Set row factory for column name access
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        yield cursor, conn  # Yield cursor and connection to be used in the repository layer
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        conn.rollback()  # Rollback in case of an error
        raise  # Re-raise the exception
    finally:
        conn.commit()  # Commit any changes if there was no exception
        conn.close()  # Close the connection to release resources
        print("Database connection closed.")
