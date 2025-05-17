import uuid
from time import sleep

from fastapi import Depends

from Processor.tts.BaseTTSProcessor import BaseTTSProcessor
from Processor.tts.impl.FakeYouProcessor import FakeYouProcessor
from Processor.tts.impl.GoogleProcessor import GoogleTTSProcessor
from dependencies.ScriptDependency import get_script_service, get_script_repo
from service.script.ScriptService import ScriptService

from service.tts.TtsTaskDispatcher import TtsTaskDispatcher


class TtsService:

    def __init__(self, repo, processor_type: str = "FakeYouTTSProcessor"):
        self.repo = repo
        self.processor = self.get_processor(processor_type)
        self.script_service = get_script_service(get_script_repo())

    @staticmethod
    def get_processor(processor_type: str) -> BaseTTSProcessor:
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
        return job_id

    def generate_audio(self, text: str, voice_id: str, job_id: str, dialogue_id: int = None):
        external_id = None
        try:
            response = self.processor.process_tts(text, voice_id, job_id)
            external_id = response["external_id"]
            self.repo.update_job(job_id, "processing", external_id)
            return {"job_id": job_id, "external_id": external_id}
        except:
            self.repo.update_job(job_id, "failed", external_id, self.processor.name)
            raise Exception("Failed to process TTS job")

    def get_status(self, job_id: str, external_id: str = None, dialogue_id: int = None):
        if external_id:
            response = self.processor.get_status(external_id)
            print(response)

            if response["status"].lower() not in ["complete_success", "complete_failure", "dead", "complete", "failed",
                                                  "success"]:
                TtsTaskDispatcher.dispatch_generate_status(job_id, external_id, self.processor.name, dialogue_id)
            self.repo.update_job(job_id, response["status"], external_id, response["result_url"])

            print(f'Updating dialogue {dialogue_id} :  job_id {job_id} and status {response["status"]}')
            self.script_service.update_dialogue_mapping(dialogue_id, job_id, response["status"])
        else:
            self.repo.get_job_status(job_id)

    def generate_script_audio(self, script_id, batch_id):
        dialogues = self.script_service.get_dialogues(script_id)
        current_batch_id = batch_id
        for i, dialogueEntry in enumerate(dialogues):
            dialogue_id = dialogueEntry["id"]
            text = dialogueEntry["dialogue"]
            tone = dialogueEntry["tone"]
            voice_id = dialogueEntry["voice_id"]
            job_id = self.create_job(text, voice_id)
            self.script_service.create_dialogue_mapping(dialogue_id, job_id, status="pending",
                                                        batch_id=current_batch_id)
            delay = (i + 1) * 45
            TtsTaskDispatcher.dispatch_tts_generation(text, voice_id, self.processor.name, dialogue_id, job_id, delay)
        return current_batch_id

    def get_cdn_url(self):
        return self.processor.get_cdn_url()

    def create_job_batch(self):
        batch_id = str(uuid.uuid4())
        self.repo.create_job_batch(batch_id)
        return batch_id

    def update_job_batch(self, batch_id, status, cdn_url=None):
        self.repo.update_job_batch(batch_id, status, cdn_url)
        pass
