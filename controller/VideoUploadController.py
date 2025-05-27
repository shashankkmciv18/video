
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import JSONResponse


from dto.VideoUploadDTO import VideoUploadRequest
from service.content_generator.VideoGenerator import generate_videos_for_platforms
from service.uploader.YoutubeUploadService import upload_to_youtube_v2
import os

router = APIRouter()
load_dotenv()


# @router.post("/video/generate-and-upload")
# async def upload_video(
#     req : VideoUploadRequest,
# ):
#     try:
#         generate_videos_for_platforms()
#     except Exception as e:
#         print("Error generating video:", e)
#         raise HTTPException(status_code=500, detail=str(e))
#
#     video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/video/short_video.mp4"))
#     print("Checking video file at:", video_path)
#     try:
#         title = req.title
#         description = req.description
#         tags = req.tags
#         video_id = upload_to_youtube_v2(
#             title=title,
#             description=description,
#             tags=tags
#         )
#         return JSONResponse(content={"videoId": video_id, "status": "Uploaded"})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.get("/video/generate-and-upload")
async def upload_video():
    try:
        generate_videos_for_platforms()
    except Exception as e:
        print("Error generating video:", e)
        raise HTTPException(status_code=500, detail=str(e))

    video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/video/short_video.mp4"))
    print("Checking video file at:", video_path)
    try:
        title = os.getenv("VIDEO_TITLE", "Daily Shorts")
        description = os.getenv("VIDEO_DESCRIPTION", "Follow for more such videos")
        tags = os.getenv("VIDEO_TAGS", "motivations,daily motivation,shorts").split(",")  # Split by comma to create a list
        video_id = upload_to_youtube_v2(
            title=title,
            description=description,
            tags=tags
        )
        return JSONResponse(content={"videoId": video_id, "status": "Uploaded"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
