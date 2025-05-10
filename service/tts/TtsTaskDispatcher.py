class TtsTaskDispatcher:

    def dispatch_generate_status(job_id: str, external_id: str, processor_type: str):
        payload = {
            "job_id": job_id,
            "external_id": external_id,
            "processor_type": processor_type
        }
        print(payload)
        # Call the Celery task to generate the status

        try:
            from eventHandler.TTSEvent import ttsEvent

            ttsEvent.apply_async(args=[payload], countdown=30)

        except Exception as e:
            print(f"Error dispatching TTS task: {e}")


