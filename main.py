from fastapi import FastAPI
from controller.YoutubeUploader import router as uploader_router
from controller.VideoGenerator import router as video_router
from controller.VideoUploadController import  router as video_upload_router
from controller.InstagramUploader import router as instagram_router
from controller.CallbackController import  router as callback_router
from controller.LLMController import  router as llmRouter
from controller.TTSController import  router as ttsRouter
from controller.ScriptController import  router as scriptRouter
from controller.MediaMergeController import  router as media_merge_router

app = FastAPI()
app.include_router(uploader_router, prefix="/api/v1", tags=["YouTube Upload"])
app.include_router(video_router, prefix="/api/v1", tags=["YouTube Upload"])
app.include_router(video_upload_router, prefix="/api/v1", tags=["YouTube Generate And Upload"])
app.include_router(instagram_router, prefix="/api/v1", tags=["Instagram Upload"])
app.include_router(callback_router, prefix="/api/v1", tags=["Callback"])
app.include_router(llmRouter, prefix="/api/v1/lang", tags=["LLM"])
app.include_router(ttsRouter, prefix="/api/v1/audio", tags=["TTS"])
app.include_router(scriptRouter, prefix="/api/v1/script", tags=["Script"])
app.include_router(media_merge_router, prefix="/api/v1/media", tags=["Media Merge"])

