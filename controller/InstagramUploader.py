import json
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Request, Depends

from dependencies.InstagramDependency import get_instagram_service
from service.uploader.InstagramUploaderService import InstagramUploaderService

router = APIRouter()
load_dotenv()



@router.post("/instagram/upload")
async def upload_video_controller(
    req: Request,
    service: InstagramUploaderService = Depends(get_instagram_service),
):
    try:
        body = json.loads((await req.body()).decode("utf-8"))
        video_url = body.get("video_url")
        caption = body.get("caption")
        response = service.upload_video(video_url, caption)
        return response

    except Exception as e:
        return {"error": str(e)}


@router.post("/instagram/publish")
async def publish_video_controller(
        req: Request,
        service: InstagramUploaderService = Depends(get_instagram_service)):
    try:
        body = await req.json()
        creation_id = body.get("creation_id")
        response = service.publish_video(creation_id)
        return response
    except Exception as e:
        return {"error": str(e)}


@router.get("/generate/post/publish")
async def generateAndPostVideo(service : InstagramUploaderService = Depends(get_instagram_service)):
    try:
        caption = os.getenv("REEL_CAPTION")
        response = service.generateAndPostVideo(caption)
        return {
            "status": "success",
            "message": "Video generated and posted successfully",
        }
    except Exception as e:
        return {"error": str(e)}
