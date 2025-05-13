import ollama
from celery.exceptions import MaxRetriesExceededError

from dependencies.PromptRepoDependency import get_prompt_repo
from eventHandler.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def llmChatEvent(self, event_data: dict):
    system_prompt = event_data.get("system_prompt")
    user_prompt = event_data.get("user_prompt")
    model = event_data.get("model")
    prompt_id = event_data["prompt_id"]
    print(f"[LLM]  ::Fetching status for {event_data}")
    # todo : use factory Stratgy for different llm, for now lets use only ollama
    try:
        response = ollama.chat(model=model, messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        response["choices"][0]["message"]["content"] = response["choices"][0]["message"]["content"].strip()
        print(f"[LLM]  Chat response: {response}")
        repo = get_prompt_repo()
        repo.update_prompt(
            id=prompt_id,
            generated_response=response["choices"][0]["message"]["content"]
        )
    except Exception as e:
        print(f"Error occurred during LLM chat: {e}")
        # Retry the task if there's an exception
        try:
            self.retry(countdown=60)  # Retry after 60 seconds
        except MaxRetriesExceededError:
            print("Max retries reached for LLM chat.")
            # Handle the situation where retry limit is exceeded






