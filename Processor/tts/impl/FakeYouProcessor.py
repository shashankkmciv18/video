import os
from dotenv import load_dotenv
import requests

from Processor.tts.BaseTTSProcessor import BaseTTSProcessor
from constants.tts.TTSConstants import FAKEYOU_API_TTS_INFERENCE, FAKEYOU_HEADERS, FAKEYOU_API_TTS_JOB

load_dotenv()


class FakeYouProcessor(BaseTTSProcessor):
    FAKEYOU_API_URL = os.getenv("FAKEYOU_API_URL", "https://api.fakeyou.com/v1/tts")
    FAKEYOU_HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self):
        super().__init__()
        self.name = "FakeYouTTSProcessor"
    def process_tts(self, text: str, voice_id: str, job_id: str):
        try:
            # Make a POST request to the FakeYou API

            response = requests.post(
                f"{self.FAKEYOU_API_URL}{FAKEYOU_API_TTS_INFERENCE}",
                headers= self.FAKEYOU_HEADERS,
                json={
                    "uuid_idempotency_token": job_id,
                    "tts_model_token": voice_id,
                    "inference_text": text
                }
            )
            print(response)

            # Handle the API response
            if response.status_code != 200:
                raise Exception(f"FakeYou API error: {response.status_code} - {response.text}")

            data = response.json()
            inference_job_token = data.get("inference_job_token")

            return {
                "job_id": job_id,
                "voice_id": voice_id,
                "external_id": inference_job_token,
            }

        except Exception as e:
            print(f"Error processing TTS with FakeYou: {e}")
            raise

    def get_status(self, inference_job_token: str):
        try:
            # Make a GET request to the FakeYou API to check the status
            response = requests.get(
                f"{self.FAKEYOU_API_URL}/{FAKEYOU_API_TTS_JOB}/{inference_job_token}",
                headers=self.FAKEYOU_HEADERS
            )
            if response.status_code != 200:
                raise Exception(f"FakeYou API error: {response.status_code} - {response.text}")
            return self.transform_tts_response(response.json())
        except Exception as e:
            raise Exception(f"Error getting status from FakeYou: {e}")

    @staticmethod
    def transform_tts_response(response):
        if not response.get("success", False):
            return {"error": "Request failed or invalid response"}

        state = response.get("state", {})
        transformed_response = {
            "job_token": state.get("job_token"),
            "status": state.get("status", "unknown"),
            "attempt_count": state.get("attempt_count", 0),
            "result_token": state.get("maybe_result_token"),
            "result_url": state.get("maybe_public_bucket_wav_audio_path"),
            "text": state.get("raw_inference_text"),
            "voice_model": state.get("model_token"),
            "created_at": state.get("created_at"),
            "updated_at": state.get("updated_at")
        }

        return transformed_response
