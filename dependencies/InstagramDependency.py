from fastapi import Depends

from db import getDB
from repository.InstagramUploadRepository import InstagramRepository
from service.uploader.InstagramUploaderService import InstagramUploaderService


def get_instagram_repository() -> InstagramRepository:
    cursor, connection = getDB()
    return InstagramRepository(cursor, connection)


def get_instagram_service(
    repo: InstagramRepository = Depends(get_instagram_repository),
) -> InstagramUploaderService:
    return InstagramUploaderService(repo)