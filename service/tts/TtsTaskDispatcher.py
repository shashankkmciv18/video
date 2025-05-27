class TtsTaskDispatcher:

    def dispatch_generate_status(job_id: str, external_id: str, processor_type: str,dialogue_id: int = None):
        payload = {
            "job_id": job_id,
            "external_id": external_id,
            "processor_type": processor_type,
            "dialogue_id": dialogue_id,
        }
        print(payload)
        # Call the Celery task to generate the status

        try:
            from eventHandler.TTSEvent import ttsEvent
            ttsEvent.apply_async(args=[payload], countdown=30)

        except Exception as e:
            print(f"Error dispatching TTS task: {e}")

    def dispatch_tts_generation(text: str, voice_id: str, processor_type: str, dialogue_id: int, job_id:str, delay: int ):
        payload = {
            "text": text,
            "voice_id": voice_id,
            "processor_type": processor_type,
            "dialogue_id": dialogue_id,
            "job_id": job_id
        }
        print(payload)
        # Call the Celery task to generate the status
        try:
            from eventHandler.TTSEvent import tts_audio_generation_event
            tts_audio_generation_event.apply_async(args=[payload], countdown=delay)
        except Exception as e:
            print(f"Error dispatching TTS task: {e}")

