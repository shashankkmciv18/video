from dotenv import load_dotenv
from fastapi import APIRouter, Request, Depends

from dependencies.AudioMergerDependency import get_audio_merger_service
from dependencies.ScriptDependency import get_script_service
from service.MergeService.AudioMergerService import AudioMergerService

router = APIRouter()
load_dotenv()


@router.post("/audio/merge")
async def merge_audio(req: Request,
                      audio_merger_service: AudioMergerService = Depends(get_audio_merger_service)
                      ):
    data = await req.json()
    batch_id = data.get("batch_id", None)

    audio_merger_service.set_processor(processor_type="FakeYouTTSProcessor")
    audio_merger_service.merge(batch_id=batch_id)
    return {
        "status": "success",
        "message": "Audio merging started",
        "batch_id": batch_id
    }
