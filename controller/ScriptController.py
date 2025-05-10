from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException

from fastapi import APIRouter, Request, Depends

from dependencies.ScriptDependency import get_script_service
from service.script.ScriptService import ScriptService

router = APIRouter()
load_dotenv()


@router.post("/store/script")
async def store_script(req: Request, scriptService: ScriptService = Depends(get_script_service)):
    data = await req.json()
    script = data.get("script")
    script_id = scriptService.save_script(script)
    return {"status": "success","script_id": script_id}