import os

from celery import Celery
from celery.exceptions import MaxRetriesExceededError

from db import getDB
from eventHandler.videoEvents.events import VideoGeneratedEvent, InstagramPostPublishedEvent

from service.uploader.InstagramUploaderService import InstagramUploaderService

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  # Or use the appropriate Redis URL if using Docker
    backend="redis://localhost:6379/0"
)


instagram_upload_service = InstagramUploaderService(getDB())


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def instagramUploadEvent(self, event_data: dict):
    print(f"[Instagram] Uploading video for {event_data['url']}")
    event = VideoGeneratedEvent(**event_data)
    url = event.url
    try:
        # Simulating Instagram upload
        response = instagram_upload_service.upload_video(event.url, os.getenv("REEL_CAPTION"))
    except Exception as e:
        print(f"Error occurred: {e}")
        try:
            self.retry(countdown=60)  # Retry after 60 seconds
        except MaxRetriesExceededError:
            print("Max retries reached for Instagram upload.")
    next_event = InstagramPostPublishedEvent(instagram_creation_id=event.response.id)
    instagramPublishEvent.apply_async(args=[next_event.dict()], countdown=30)
    print(f"[Instagram] Video upload process started successfully for {event.url}")



@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def instagramPublishEvent(self, event_data: dict):
    print(f"[Follow-up] Instagram post for video {event_data['instagram_creation_id']} is now live")
    event = InstagramPostPublishedEvent(**event_data)
    try:
        response = instagram_upload_service.publish_video(event.instagram_content_id)
    except Exception as e:
        print(f"Error occurred: {e}")
        try:
            self.retry(countdown=60)  # Retry after 60 seconds
        except MaxRetriesExceededError:
            print("Max retries reached for Instagram upload.")
    print(f"[Follow-up] Instagram post for video {event.instagram_creation_id} is now live at {response.id}")
