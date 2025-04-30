from pydantic import BaseModel


class VideoUploadRequest(BaseModel):
    title: str
    description: str
    tags: list[str]