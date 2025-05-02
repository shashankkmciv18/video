from fastapi import FastAPI
from controller.YoutubeUploader import router as uploader_router
from controller.VideoGenerator import router as video_router
from controller.VideoUploadController import  router as video_upload_router
from controller.InstagramUploader import router as instagram_router
app = FastAPI()
app.include_router(uploader_router, prefix="/api/v1", tags=["YouTube Upload"])
app.include_router(video_router, prefix="/api/v1", tags=["YouTube Upload"])
app.include_router(video_upload_router, prefix="/api/v1", tags=["YouTube Generate And Upload"])
app.include_router(instagram_router, prefix="/api/v1", tags=["Instagram Upload"])