# file: service/tts/processors/GoogleTTSProcessor.py
import os

from Processor.tts.BaseTTSProcessor import BaseTTSProcessor


class GoogleTTSProcessor(BaseTTSProcessor):

    def __init__(self):
        super().__init__()
        self.name = "GoogleTTSProcessor"
    def process_tts(self, text: str, voice_id: str, job_id: str):
        raise NotImplementedError("Google TTS does not support processing.")

    def get_status(self, job_id: str):
        raise NotImplementedError("Google TTS does not support status checking.")

    def get_cdn_url(self):
        return os.getenv("GOOGLE_CDN_URL", "https://default-google-cdn-url.com")