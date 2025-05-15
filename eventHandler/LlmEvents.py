import json

import ollama
from celery.exceptions import MaxRetriesExceededError

from dependencies.ScriptDependency import get_script_service, get_script_repo
from dependencies.TTSDependency import get_tts_service, get_tts_repo
from eventHandler import ttsEvent
from eventHandler.celery_app import celery_app


# @celery_app.task(bind=True, max_retries=3, default_retry_delay=120)
def llmChatEvent(event_data: dict):
    print("[LLM]  ::Fetching status for {event_data}")
    system_prompt = event_data.get("system_prompt")
    user_prompt = event_data.get("user_prompt")
    model = event_data.get("model")
    prompt_id = event_data["prompt_id"]
    weights = event_data.get("weights")
    # todo : use factory Stratgy for different llm, for now lets use only ollama
    try:
        response = ollama.chat(model=model, messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ], format = 'json')
        try:
            try:
                content_str = response["message"]["content"].strip()
            except Exception as e:
                raise  Exception(f"Error accessing message content: {e}")
            script_service = get_script_service(get_script_repo())
            try:
                script = json.loads(content_str)
                script_id = script_service.save_script(script, weights, prompt_id)
                print(f"Script ID: {script_id}")
                tts_service = get_tts_service(get_tts_repo())
                tts_service.generate_script_audio(script_id)
            except Exception as e:
                print(f"Error saving script: {e}")
        except Exception as e:
            print(f"Error converting response to JSON: {e}")
    except Exception as e:
        print(f"Error occurred during LLM chat: {e}")
        # Retry the task if there's an exception
        try:
            self.retry(countdown=60)  # Retry after 60 seconds
        except MaxRetriesExceededError:
            print("Max retries reached for LLM chat.")
            # Handle the situation where retry limit is exceeded






