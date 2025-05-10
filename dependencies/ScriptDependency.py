from fastapi import Depends

from db import getDB
from repository.ScriptRepository import ScriptRepository
from service.script.ScriptService import ScriptService


def get_script_repo() -> ScriptRepository:
    cursor, connection = getDB()
    return ScriptRepository(cursor, connection)

def get_script_service(
        repo: ScriptRepository = Depends(get_script_repo),

) -> ScriptService:
    return ScriptService(repo)