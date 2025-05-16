import json
import ollama
from celery.exceptions import MaxRetriesExceededError
from openai import OpenAI

from dependencies.ScriptDependency import get_script_service, get_script_repo
from dependencies.TTSDependency import get_tts_repo, get_tts_service
from eventHandler.celery_app import celery_app
from service.language.LLMHelper import chat_with_openrouter

tts_service = get_tts_service(get_tts_repo())
script_service = get_script_service(get_script_repo())


@celery_app.task(bind=True, max_retries=3, default_retry_delay=120, name="llmChatEvent", queue="youtube")
def llmChatEvent(self, event_data: dict):
    print(f"[LLM]  ::Fetching status for {event_data}")
    system_prompt = event_data.get("system_prompt")
    user_prompt = event_data.get("user_prompt")
    model = event_data.get("model")
    prompt_id = event_data["prompt_id"]
    weights = event_data.get("weights")
    client_id = event_data.get("client_id")

    try:

        client_url = ''
        api_key = ''
        # todo fetch from DB

        client = OpenAI(
            base_url= client_url,
            api_key=api_key,
        )
        response = chat_with_openrouter(client, system_prompt, user_prompt, model)
        content_str = extract_message_content(response)
        script_id = save_script_from_content(content_str, weights, prompt_id)
        batch_id = generate_audio_and_enqueue(script_id)
    except Exception as e:
        print(f"Error occurred during LLM chat: {e}")
        try:
            self.retry(countdown=60)
        except MaxRetriesExceededError:
            print("Max retries reached for LLM chat.")


def extract_message_content(response):
    try:
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error accessing message content: {e}")


def save_script_from_content(content_str, weights, prompt_id):
    try:

        script = json.loads(content_str)
        script_id = script_service.save_script(script, weights, prompt_id)
        print(f"Script ID: {script_id}")
        return script_id
    except Exception as e:
        print(f"Error saving script: {e}")
        raise


def generate_audio_and_enqueue(script_id):
    try:
        batch_id = tts_service.generate_script_audio(script_id)
        from AudioEvents import check_and_merge_audio_event
        check_and_merge_audio_event.apply_async(args=[batch_id])
        return batch_id
    except Exception as e:
        print(f"Error generating audio or enqueuing merge event: {e}")
