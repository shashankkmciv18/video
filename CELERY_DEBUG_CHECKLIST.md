# Celery Task Registration & Execution Debug Checklist

## 1. Ensure Task Module is Imported

Celery only registers tasks that are imported when the worker starts.  
**In `/eventHandler/__init__.py` add:**
```python
from .LlmEvents import *
```
This ensures `llmChatEvent` is registered.

---

## 2. Confirm Celery Autodiscovery

In `/eventHandler/celery_app.py`, you have:
```python
celery_app.autodiscover_tasks([
    "eventHandler.TTSEvent",
    "eventHandler.AdditionEvent",
    "eventHandler.AudioEvents",
    "eventHandler.LlmEvents",
])
```
- Make sure the module names match the actual Python files (case-sensitive, no typos).
- If your tasks are in `eventHandler/LlmEvents.py`, the entry should be `"eventHandler.LlmEvents"`.

---

## 3. Task Decorator and Name

In `/eventHandler/LlmEvents.py`:
```python
@celery_app.task(bind=True, max_retries=3, default_retry_delay=120, name="llmChatEvent", queue="youtube")
def llmChatEvent(self, event_data: dict):
    ...
```
- The `name` should match the routing key in `task_routes`.
- The `queue` argument is optional if you use routing.

---

## 4. Task Routing

In `/eventHandler/celery_app.py`:
```python
celery_app.conf.task_routes = {
    'llmChatEvent': {'queue': YOUTUBE_QUEUE},
}
```
- Ensure `YOUTUBE_QUEUE = 'youtube'` is defined above.

---

## 5. Start Worker with Correct Queue

Start your worker with:
```bash
celery -A eventHandler.celery_app worker -Q youtube --loglevel=DEBUG
```
- This ensures the worker listens to the `youtube` queue.

---

## 6. Call the Task

When you want to enqueue the task:
```python
from eventHandler.LlmEvents import llmChatEvent
llmChatEvent.apply_async(args=[event_data])
# or
llmChatEvent.delay(event_data)
```
- Make sure this line is executed.

---

## 7. Debugging

- Add a print statement at the top of `llmChatEvent` to confirm execution.
- Check Celery worker logs for task registration and execution.

---

## 8. Example Minimal Working Setup

**/eventHandler/__init__.py**
```python
from .LlmEvents import *
```

**/eventHandler/celery_app.py**
```python
from celery import Celery
from kombu import Queue, Exchange

YOUTUBE_QUEUE = 'youtube'

celery_app = Celery(
    "eventHandler",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.task_queues = (
    Queue(YOUTUBE_QUEUE, Exchange(YOUTUBE_QUEUE, type='direct'), routing_key=YOUTUBE_QUEUE),
)

celery_app.conf.task_routes = {
    'llmChatEvent': {'queue': YOUTUBE_QUEUE},
}

celery_app.autodiscover_tasks([
    "eventHandler.LlmEvents",
])
```

**/eventHandler/LlmEvents.py**
```python
from .celery_app import celery_app

@celery_app.task(bind=True, name="llmChatEvent")
def llmChatEvent(self, event_data: dict):
    print("llmChatEvent triggered with:", event_data)
```

---

## 9. If Still Not Working

- Double-check all file/module names and imports.
- Restart the worker after any code changes.
- Run `celery -A eventHandler.celery_app inspect registered` to see if your task is registered.

---

**If you follow these steps and ensure all modules are imported and named correctly, your Celery task will be registered and executed.**