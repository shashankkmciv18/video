import json
import os

from fastapi import APIRouter, Request

from db import get_db, get_db_1
from repository.InstagramUploadRepository import InstagramRepository
from service.uploader.InstagramUploaderService import InstagramUploaderService

router = APIRouter()


@router.post("/instagram/upload")
async def upload_video_controller(req: Request):
    try:
        body = json.loads((await req.body()).decode("utf-8"))
        video_url = body.get("video_url")
        caption = body.get("caption")

        db_cursor, db_connection = get_db_1()
        repo = InstagramRepository(db_cursor, db_connection)

        service = InstagramUploaderService(repo)
        response = service.upload_video(video_url, caption)
        return response

    except Exception as e:
        return {"error": str(e)}




@router.post("/instagram/publish")
async def publish_video_controller(req: Request):
    try:
        body = await req.json()
        creation_id = body.get("creation_id")
        db_cursor, db_connection = get_db_1()
        repo = InstagramRepository(db_cursor, db_connection)
        service = InstagramUploaderService(repo)
        response = service.publish_video(creation_id)
        return response
    except Exception as e:
        return {"error": str(e)}