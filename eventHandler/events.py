from pydantic import BaseModel


class VideoGeneratedEvent(BaseModel):
    path: str
    url: str


class InstagramPostPublishedEvent(BaseModel):
    instagram_creation_id: str
