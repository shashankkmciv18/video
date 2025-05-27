import logging

from eventHandler.celery_app import celery_app

# Setup a logger
logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def addEvent(self, event_data: dict):
    print(f"[Addition] Generating audio for: {event_data}")
    # Example logic
    job_id = event_data.get("job_id")
    external_id = event_data.get("external_id")
    processor_type = event_data.get("processor_type")
    logger.info(f"Processing TTS event: {event_data}")
    logger.info(f"Job ID: {job_id}, External ID: {external_id}, Processor: {processor_type}")
    # Simulate TTS generation
    # Here you would typically call your TTS service to generate audio


    print(f"Job ID: {job_id}, External ID: {external_id}, Processor: {processor_type}")


