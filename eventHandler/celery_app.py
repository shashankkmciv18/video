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
    Queue('audio_queue', Exchange('audio_queue', type='direct'), routing_key='audio_queue'),
)
# Autodiscover tasks in the flat eventHandler module
celery_app.autodiscover_tasks([
    # "eventHandler.YoutubeEvent",
    # "eventHandler.InstagramEvent",
    "eventHandler.TTSEvent",
    "eventHandler.AdditionEvent",
    "eventHandler.AudioEvents",
])

# Define routing for specific tasks
celery_app.conf.task_routes = {
    # 'eventHandler.YoutubeEvent.youtubeEvent': {'queue': 'youtube'},
    # 'eventHandler.InstagramEvent.instagramUploadEvent': {'queue': 'youtube'},
    'eventHandler.TTSEvent.ttsEvent': {'queue': 'youtube'},
    'eventHandler.TTSEventNew.ttsEvent': {'queue': 'youtube'},
    'eventHandler.AdditionEvent.addEvent': {'queue': 'youtube'},
    'eventHandler.TTSEvent.tts_audio_generation_event': {'queue': 'youtube'},
    'eventHandler.AudioEvents.audio_merge_task': {'queue': 'audio_queue'},

}
