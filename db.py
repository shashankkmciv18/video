import sqlite3
import os
from contextlib import contextmanager

_db_connection = None
_db_cursor = None


def getDB():
    global _db_connection, _db_cursor
    if _db_connection is None or _db_cursor is None:
        _db_connection = sqlite3.connect("database.db", check_same_thread=False)
        _db_cursor = _db_connection.cursor()
    return _db_cursor, _db_connection


