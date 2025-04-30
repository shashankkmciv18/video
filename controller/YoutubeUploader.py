from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse

from dto.VideoUploadDTO import VideoUploadRequest
from service.uploader.YoutubeUploadService import upload_to_youtube_v2
import os
router = APIRouter()

@router.post("/youtube")
async def upload_video(
    req : VideoUploadRequest,
):
    try:
        video_id = upload_to_youtube_v2(req)
        return JSONResponse(content={"videoId": video_id, "status": "Uploaded"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
