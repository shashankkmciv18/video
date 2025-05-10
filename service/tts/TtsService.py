import uuid
from time import sleep

from Processor.tts.BaseTTSProcessor import BaseTTSProcessor
from Processor.tts.impl.FakeYouProcessor import FakeYouProcessor
from Processor.tts.impl.GoogleProcessor import GoogleTTSProcessor

from service.tts.TtsTaskDispatcher import TtsTaskDispatcher


class TtsService:
    def __init__(self, repo, processor_type: str = "FakeYouTTSProcessor"):
        self.repo = repo
        self.processor = self._get_processor(processor_type)

    @staticmethod
    def _get_processor(processor_type: str) -> BaseTTSProcessor:
        if processor_type == "FakeYouTTSProcessor":
            return FakeYouProcessor()
        elif processor_type == "GoogleTTSProcessor":
            return GoogleTTSProcessor()
        else:
            raise ValueError(f"Unsupported processor type: {processor_type}")

    @staticmethod
    def _generate_job_id():
        return str(uuid.uuid4())

    def get_current_processor(self):
        return self.processor.__class__.__name__

    def create_job(self, text: str, voice_id: str):
        # Create a new TTS job in the database
        job_id = self._generate_job_id()
        status = "pending"
        processor = self.processor.get_name()
        self.repo.create_job_entry(text, voice_id, job_id, status, processor)
        self.generate_audio(text, voice_id, job_id)
        return job_id



    def generate_audio(self, text: str, voice_id: str, job_id: str):
        external_id = None
        try:
            response = self.processor.process_tts(text, voice_id, job_id)
            external_id = response["external_id"]
            self.repo.update_job(job_id, "processing", external_id)
            TtsTaskDispatcher.dispatch_generate_status(job_id, external_id, self.processor.name)
            # sleep(50)
            self.get_status(job_id, external_id)
        except:
            self.repo.update_job(job_id, "failed", external_id, self.processor.name)
            raise Exception("Failed to process TTS job")

    def get_status(self, job_id: str, external_id: str = None):
        if external_id:
            response = self.processor.get_status(external_id)
            print(response)

            if response["status"].lower() != "complete_success":
                TtsTaskDispatcher.dispatch_generate_status(job_id, external_id, self.processor.name)
            self.repo.update_job(job_id, response["status"], external_id, response["result_url"])
        else:
            self.repo.get_job_status(job_id)
