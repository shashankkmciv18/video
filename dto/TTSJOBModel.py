from pydantic import BaseModel
from enum import Enum

class JobStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class CreateJobRequest(BaseModel):
    text: str
    voice_id: str

class CreateJobResponse(BaseModel):
    job_id: str
    status: JobStatus
