from celery import Celery
from kombu import Queue, Exchange

celery_app = Celery(
    "eventHandler",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Kolkata',
    enable_utc=False,
)

# Declare the 'youtube' queue

celery_app.conf.task_queues = (
    Queue('youtube', Exchange('youtube', type='direct'), routing_key='youtube'),
)
# Autodiscover tasks in the flat eventHandler module
celery_app.autodiscover_tasks([
    # "eventHandler.YoutubeEvent",
    # "eventHandler.InstagramEvent",
    "eventHandler.TTSEvent",
    "eventHandler.AdditionEvent",
    "eventHandler.TTSEventNew",
])

# Define routing for specific tasks
celery_app.conf.task_routes = {
    # 'eventHandler.YoutubeEvent.youtubeEvent': {'queue': 'youtube'},
    # 'eventHandler.InstagramEvent.instagramUploadEvent': {'queue': 'youtube'},
    'eventHandler.TTSEvent.ttsEvent': {'queue': 'youtube'},
    'eventHandler.TTSEventNew.ttsEvent': {'queue': 'youtube'},
    'eventHandler.AdditionEvent.addEvent': {'queue': 'youtube'},
}
