

import requests
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import JSONResponse


from dto.VideoUploadDTO import VideoUploadRequest
from service.content_generator.VideoGenerator import generate_videos_for_platforms
from service.uploader.YoutubeUploadService import upload_to_youtube_v2
import os
router = APIRouter()


APP_ID = "1390764348744729"
APP_SECRET = "3b2b30021500ac520c5d30d0f5ca1954"
REDIRECT_URI = "https://8346-2405-201-600d-500f-49fc-bac2-8cd4-34e6.ngrok-free.app/api/v1/auth/callback"


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


@router.get("/auth/callback")
def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing authorization code from Facebook"}

    token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }

    token_res = requests.get(token_url, params=params)
    if token_res.status_code != 200:
        return {"error": "Failed to fetch access token", "details": token_res.text}

    access_token = token_res.json().get("access_token")
    print(access_token)
    return {
        "message": "Short-lived access token retrieved successfully",
        "access_token": access_token,
    }