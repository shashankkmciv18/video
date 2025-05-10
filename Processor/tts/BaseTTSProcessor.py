# file: service/tts/processors/BaseTTSProcessor.py
from abc import ABC, abstractmethod

class BaseTTSProcessor(ABC):
    
    def __init__(self):
        self.name = None
    @abstractmethod
    def process_tts(self, text: str, voice_id: str, job_id: str):
        pass

    @abstractmethod
    def get_status(self, param):
        pass
    
    def get_name(self):
        pass