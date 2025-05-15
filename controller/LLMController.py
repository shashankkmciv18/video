from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request

from dto.OllamaModel import ChatRequest
from service.language.LanguageService import LanguageService

router = APIRouter()
load_dotenv()


languageService = LanguageService()

@router.post("/v1/chat/completions")
def chat(req: ChatRequest):
    result = languageService.chat(req.messages, req.model, req.weights)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result