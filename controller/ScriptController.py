from fastapi import FastAPI, Depends, HTTPException

from fastapi import APIRouter, Request, Depends

router = APIRouter()
load_dotenv()


@router.post("/store/script")
async def store_script(req: Request):
    data = await req.json()
    script = data.get("script")
    video_id = data.get("video_id")
    # Save the script to the database or file system
    # For now, we'll just return it
    return {"script": script, "video_id": video_id}