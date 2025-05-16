from celery import Celery
from kombu import Queue, Exchange

# Define queue names as constants for easier maintenance
YOUTUBE_QUEUE = 'youtube'
AUDIO_QUEUE = 'audio_queue'
LLM_QUEUE = 'llm'

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

# Define queues with their exchanges and routing keys
celery_app.conf.task_queues = (
    Queue(YOUTUBE_QUEUE, Exchange(YOUTUBE_QUEUE, type='direct'), routing_key=YOUTUBE_QUEUE),
    Queue(AUDIO_QUEUE, Exchange(AUDIO_QUEUE, type='direct'), routing_key=AUDIO_QUEUE),
    Queue(LLM_QUEUE, Exchange(LLM_QUEUE, type='direct'), routing_key=LLM_QUEUE),
)
# Autodiscover tasks in the flat eventHandler module
celery_app.autodiscover_tasks([
    # "eventHandler.YoutubeEvent",
    # "eventHandler.InstagramEvent",
    "eventHandler.TTSEvent",
    "eventHandler.AdditionEvent",
    "eventHandler.AudioEvents",
    "eventHandler.LlmEvents",
])

# Celery task routing configuration
celery_app.conf.task_routes = {
    # TTS Events
    'eventHandler.TTSEvent.ttsEvent': {'queue': YOUTUBE_QUEUE},
    'eventHandler.TTSEventNew.ttsEvent': {'queue': YOUTUBE_QUEUE},
    'eventHandler.TTSEvent.tts_audio_generation_event': {'queue': YOUTUBE_QUEUE},

    # Addition Event
    'eventHandler.AdditionEvent.addEvent': {'queue': YOUTUBE_QUEUE},

    # Audio Merge Task
    'eventHandler.AudioEvents.audio_merge_task': {'queue': AUDIO_QUEUE},
    'eventHandler.AudioEvents.check_and_merge_audio_event': {'queue': AUDIO_QUEUE},

    # LLM Chat Event
    'eventHandler.LlmEvents.llmChatEvent': {'queue': YOUTUBE_QUEUE},

}

# NOTE:
# - Ensure the task names above match the 'name' parameter in your @celery_app.task decorators.
# - If you use custom task names (e.g., name="audio_merge_task"), use that name as the key.
# - Commented routes are preserved for reference but not currently active.
