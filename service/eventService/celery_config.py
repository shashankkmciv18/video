from celery import Celery

celery_app = Celery(
    "eventHandler",  # You can use your app's module name here
    broker="redis://localhost:6379/0",  # Adjust Redis connection
    backend="redis://localhost:6379/0"
)

from eventHandler.videoEvents.YoutubeTasks import test_task, youtubeEvent
from eventHandler.videoEvents.InstagramTasks import instagramUploadEvent



# Route tasks to specific queues if necessary

celery_app.conf.task_routes = {
    instagramUploadEvent: {'queue': 'youtube'},
    youtubeEvent: {'queue': 'youtube'},
    test_task: {'queue': 'youtube'}
}
