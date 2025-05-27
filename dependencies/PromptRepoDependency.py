from db import getDB
from repository.PromptRepository import PromptRepository


def get_prompt_repo():
    cursor, connection = getDB()
    return PromptRepository(cursor, connection)
