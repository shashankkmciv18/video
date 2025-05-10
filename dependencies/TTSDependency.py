from fastapi import Depends

from db import getDB
from repository.TtsRepository import TtsRepository
from service.tts.TtsService import TtsService


def get_tts_repo() -> TtsRepository:
    cursor, connection = getDB()
    return TtsRepository(cursor, connection)


def get_tts_service(
        repo: TtsRepository = Depends(get_tts_repo),
        processor_type: str = "FakeYouTTSProcessor"
) -> TtsService:
    return TtsService(repo, processor_type)
