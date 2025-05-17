from fastapi import Depends

from repository.LlmClientRepository import LlmClientRepository
from service.language.LlmClientService import LlmClientService


def get_llm_client_repo():
    return LlmClientRepository()


def get_llm_client_service(repo: LlmClientRepository = Depends(get_llm_client_repo),
) -> LlmClientService:
    return LlmClientService(repo)
