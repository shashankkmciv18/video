
import time
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse

from dto.VideoUploadDTO import VideoUploadRequest
from service.content_generator.VideoGenerator import generate_videos_for_platforms
from service.uploader.YoutubeUploadService import upload_to_youtube_v2
import os
router = APIRouter()

@router.post("/video/generate-and-upload")
async def upload_video(
    req : VideoUploadRequest,
):

    try:
        generate_videos_for_platforms()
    except Exception as e:
        print("Error generating video:", e)
        raise HTTPException(status_code=500, detail=str(e))

    video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/video/short_video.mp4"))
    print("Checking video file at:", video_path)
    try:
        video_id = upload_to_youtube_v2(req)
        return JSONResponse(content={"videoId": video_id, "status": "Uploaded"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
