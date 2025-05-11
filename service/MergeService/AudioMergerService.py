import os

from dependencies.ScriptDependency import get_script_repo, get_script_service
from dependencies.TTSDependency import get_tts_service, get_tts_repo
from eventHandler.AudioEvents import download_and_merge_audio, helper


class AudioMergerService:
    def __init__(self):
        self.script_service = get_script_service(get_script_repo())
        self.tts_service = get_tts_service(get_tts_repo())

    def set_processor(self, processor_type: str):
        # Set the TTS processor type
        self.tts_service.processor = self.tts_service.get_processor(processor_type)

    def fetch(self, batch_id: list[str]):
        audio_entries = self.script_service.fetch_audio_entries(batch_id)
        return audio_entries

    def merge(self, batch_id: list):
        entries = self.fetch(batch_id=batch_id)
        relative_output_path = os.getenv("OUTPUT_PATH")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(script_dir))
        output_path = os.path.join(root_dir, relative_output_path)


        payload = {
            "entries": entries,
            "output_path": output_path,
            "cdn_host": self.tts_service.get_cdn_url()
        }
        download_and_merge_audio.apply_async(args=[payload], countdown=5)



    def save_audio(self, merged_audio, output_path: str):
        # Save the merged audio to the specified path
        with open(output_path, 'wb') as f:
            f.write(merged_audio)
