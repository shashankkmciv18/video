from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from dto.VideoUploadDTO import VideoUploadRequest
from service.uploader.YoutubeUploadService import upload_to_youtube_v2, generate_token

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
