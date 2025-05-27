import time

from celery.exceptions import MaxRetriesExceededError

from eventHandler.celery_app import celery_app
from eventHandler.events import VideoGeneratedEvent
from service.uploader.YoutubeUploadService import default_youtube_upload


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def youtubeEvent(self, event_data: dict):
    print(f"[YouTube] Uploading video for {event_data['path']}")
    event = VideoGeneratedEvent(**event_data)
    try:
        # Simulate YouTube upload
        default_youtube_upload()
    except Exception as e:
        print(f"Error occurred during YouTube upload: {e}")
        # Retry the task if there's an exception
        try:
            self.retry(countdown=60)  # Retry after 60 seconds
        except MaxRetriesExceededError:
            print("Max retries reached for YouTube upload.")
            # Handle the situation where retry limit is exceeded
    print(f"[YouTube] Video upload process started successfully for {event.path}")


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def test_task(event_data: dict):
    event = VideoGeneratedEvent(**event_data)
    print("Starting Test Event Task")
    time.sleep(30)
    print(f"Test task executed {event.video_id} with path {event.video_path}")