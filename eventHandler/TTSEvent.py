from celery.exceptions import MaxRetriesExceededError
from fastapi import Depends

from dependencies.ScriptDependency import get_script_service, get_script_repo
from eventHandler.celery_app import celery_app
from dependencies.TTSDependency import get_tts_service


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def ttsEvent(self, event_data: dict):
    print(f"[TTS]  ::Fetching status for {event_data}")
    event = event_data
    try:
        from dependencies.TTSDependency import get_tts_repo
        from service.tts.TtsService import TtsService

        repo = get_tts_repo()  # Create the repository instance
        tts_service = TtsService(repo, event['processor_type'])
        # Simulate TTS generation
        tts_service.get_status(event["job_id"], event["external_id"], event["dialogue_id"])
    except Exception as e:
        print(f"Error occurred during TTS generation: {e}")
        # Retry the task if there's an exception
        try:
            self.retry(countdown=60)  # Retry after 60 seconds
        except MaxRetriesExceededError:
            print("Max retries reached for TTS generation.")
            # Handle the situation where retry limit is exceeded
    print(f"[TTS]  Fetching Status successful")


@celery_app.task(bind=True, max_retries=2, default_retry_delay=60)
def tts_audio_generation_event(self, event_data: dict):
    print(f"[TTS] TTS ::Generating audio for {event_data}")
    event = event_data
    try:
        from dependencies.TTSDependency import get_tts_repo
        from service.tts.TtsService import TtsService
        repo = get_tts_repo()  # Create the repository instance
        tts_service = TtsService(repo, event['processor_type'])
        # Simulate TTS generation
        response = tts_service.generate_audio(event["text"], event["voice_id"], event["job_id"], event["dialogue_id"])
        tts_service.get_status(event["job_id"], response["external_id"], event["dialogue_id"])

    except Exception as e:
        print(f"Error occurred during TTS generation: {e}")
        # Retry the task if there's an exception
        try:
            self.retry(countdown=60)  # Retry after 60 seconds
        except MaxRetriesExceededError:
            print("Max retries reached for TTS generation.")
            # Handle the situation where retry limit is exceeded
    print(f"[TTS] Audio generation process started successfully")
