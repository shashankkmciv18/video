from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse

from service.content_generator.VideoGenerator import generate_videos_for_platforms

router = APIRouter()


@router.get("/generate")
async def generate(

):
    try:
        path = generate_videos_for_platforms()
        return JSONResponse(content={"path": path, "status": "Created"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
