from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse

from dto.VideoUploadDTO import VideoUploadRequest
from service.content_generator.VideoGenerator import generate_videos_for_platforms
from service.uploader.YoutubeUploadService import upload_to_youtube_v2, generate_token
import os
router = APIRouter()

@router.post("/youtube")
async def upload_video(
    req : VideoUploadRequest,
):
    try:
        title = req.title
        description = req.description
        tags = req.tags
        video_id = upload_to_youtube_v2(
            title=title,
            description=description,
            tags=tags
        )
        return JSONResponse(content={"videoId": video_id, "status": "Uploaded"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/token")
async def generate_token_controller():
    generate_token()
