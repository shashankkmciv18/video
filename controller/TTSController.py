from fastapi import FastAPI, Depends, HTTPException

from fastapi import APIRouter, Request, Depends

from dependencies.ScriptDependency import get_script_service
from dependencies.TTSDependency import get_tts_service
from service.script.ScriptService import ScriptService
from service.tts.TtsService import TtsService

router = APIRouter()

@router.post("/generate")
async def create_job(req: Request, tts_service: TtsService = Depends(get_tts_service)):
    data = await req.json()  # Await the asynchronous method
    text = data.get("text")
    voice_id = data.get("voice_id")


    job = tts_service.create_job(text, voice_id)
    if not job:
        raise HTTPException(status_code=500, detail="Failed to create job")

    return {"job_id": job.job_id}


@router.post("/status")
async def get_status(req: Request, tts_service: TtsService = Depends(get_tts_service)):
    data = await req.json()
    job_id = data.get("job_id")
    ext_id = data.get("external_id")

    status = tts_service.get_status(job_id, ext_id)
    # if not status:
    #     raise HTTPException(status_code=404, detail="Job not found")

    return {"status": status}


@router.post("/generate/script/audio")
async def generate_script_audio(req: Request, tts_service: TtsService = Depends(get_tts_service)):

    data = await req.json()
    script_id = data.get("script_id")
    tts_service.generate_script_audio(script_id)
    return {"message": "Audio generation started for the script."}
