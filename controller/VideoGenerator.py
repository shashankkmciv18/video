import os.path

from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse

from eventHandler.videoEvents.InstagramTasks import instagramUploadEvent
from eventHandler.videoEvents.YoutubeTasks import youtubeEvent, test_task
from eventHandler.videoEvents.events import VideoGeneratedEvent

from service.content_generator.VideoGenerator import generate_videos_for_platforms
from service.uploader.S3UploaderService import S3UploaderService

router = APIRouter()


@router.get("/generate")
async def generate(

):
    try:
        file_path = generate_videos_for_platforms()
        s3_uploader_service = S3UploaderService()
        upload_url = s3_uploader_service.upload_file_to_s3(file_path=file_path)
        # This is used to mock the video generation
        # file_path = os.path.join(os.path.dirname(__file__), "../resources/video/short_video.mp4")
        # upload_url = 'https://videogenerator001.s3.us-east-1.amazonaws.com/videos/short_video.mp4'
        youtubeEvent.apply_async(args=[{"path": file_path, 'url': upload_url}], coundown=30)
        instagramUploadEvent.apply_async(args=[{"url": upload_url, "path": file_path}], coundown=30)
        return JSONResponse(content={"url": upload_url, "status": "Processing"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
