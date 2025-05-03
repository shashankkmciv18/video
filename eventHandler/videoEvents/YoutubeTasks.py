import time

from celery import Celery
from celery.exceptions import MaxRetriesExceededError

from eventHandler.videoEvents.events import VideoGeneratedEvent
from service.uploader.YoutubeUploadService import default_youtube_upload

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  # Or use the appropriate Redis URL if using Docker
    backend="redis://localhost:6379/0"
)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)  # Retry up to 3 times with a 60s delay
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


@celery_app.task
def test_task(event_data: dict):
    event = VideoGeneratedEvent(**event_data)
    print("Starting Test Event Task")
    time.sleep(30)
    print(f"Test task executed {event.video_id} with path {event.video_path}")