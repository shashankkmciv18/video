import os


from celery.exceptions import MaxRetriesExceededError

from eventHandler.celery_app import celery_app
from dependencies.InstagramDependency import get_instagram_service
from eventHandler.events import VideoGeneratedEvent, InstagramPostPublishedEvent

instagram_upload_service = get_instagram_service()


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def instagramUploadEvent(self, event_data: dict):

    event = VideoGeneratedEvent(**event_data)
    print(f"[Instagram] Uploading video  {event.url}")
    try:
        # Simulating Instagram upload
        response = instagram_upload_service.upload_video(event.url, os.getenv("REEL_CAPTION"))
        print(f"response : {response}")
        next_event = InstagramPostPublishedEvent(instagram_creation_id=response["id"])
        print(next_event.dict())

        instagramPublishEvent.apply_async(args=[next_event.dict()], countdown=30)
        print(f"[Instagram] Video upload process started successfully for {response['id']}")
    except Exception as e:
        print(f"Error occurred: {e}")
        try:
            self.retry(countdown=60)  # Retry after 60 seconds
        except MaxRetriesExceededError:
            print("Max retries reached for Instagram upload.")





@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def instagramPublishEvent(self, event_data: dict):
    event = InstagramPostPublishedEvent(**event_data)
    print(f"[Follow-up] Instagram post for video {event.instagram_creation_id} is now live")
    try:
        creation_id = event.instagram_creation_id
        print('creation_id : ', creation_id)
        response = instagram_upload_service.publish_video(creation_id)
        print(f"[Follow-up] Instagram post for video {event.instagram_creation_id}")
    except Exception as e:
        print(f"Error occurred: {e}")
        try:
            self.retry(countdown=60)  # Retry after 60 seconds
        except MaxRetriesExceededError:
            print("Max retries reached for Instagram upload.")