import os
import tempfile
import uuid
import subprocess
import requests

from eventHandler.celery_app import celery_app
from service.uploader.S3UploaderService import S3UploaderService

from celery import shared_task
from dependencies.ScriptDependency import get_script_service, get_script_repo
from dependencies.TTSDependency import get_tts_service, get_tts_repo
from service.MergeService.AudioMergerService import AudioMergerService
from service.MergeService.MergerHelper import  helper

script_service = get_script_service(get_script_repo())
tts_service = get_tts_service(get_tts_repo())
merger_service = AudioMergerService()


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60, name="audio_merge_task", queue="audio_queue")
def download_and_merge_audio(self, event_data: dict):
# def download_and_merge_audio(event_data: dict):
    """
    entries: List of dictionaries with keys:
        - 'status': Status of the audio file (e.g., 'complete_success')
        - 'seq_id': Sequence ID to determine the order
        - 'voice_url': Path to the audio file on the CDN
        - 'pause_seconds': Duration of pause after the audio file
    cdn_host: Base URL of the CDN (e.g., 'https://cdn.example.com')
    output_dir: Directory where the merged audio file will be saved
    """

    path = helper(event_data=event_data)
    if path:
        s3_uploader_service = S3UploaderService()
        s3_file_key = f"audio/{os.path.basename(path)}"
        print(f"Uploading {path} to S3 with key {s3_file_key}")
        upload_url = s3_uploader_service.upload_file_to_s3(file_path=path, s3_file_key=s3_file_key)
        if upload_url:
            print(event_data)
            tts_service.update_job_batch(event_data["batch_id"], "complete_success", upload_url)
        print(f"File uploaded to S3: {upload_url}")


@celery_app.task(bind=True, max_retries=10, default_retry_delay=60, name="check_and_merge_audio_event", queue="audio_queue")
def check_and_merge_audio_event(self, batch_id):
    # Fetch all audio entries for the batch
    entries = merger_service.fetch(batch_id)
    if not entries:
        print(f"No entries found for batch {batch_id}")
        return

    # Check if all jobs are successful
    all_success = all(entry.get("status") == "complete_success" for entry in entries)

    if all_success:
        print(f"All jobs in batch {batch_id} are successful. Merging audio.")

        merger_service.merge(batch_id)
    else:
        try:
            # Exponential backoff: delay = default_retry_delay * (2 ** (retry_count - 1))
            base_delay = self.default_retry_delay or 60
            retry_count = self.request.retries + 1  # retries is 0-based
            delay = base_delay * (2 ** (retry_count - 1))
            print(
                f"Not all jobs in batch {batch_id} are complete. Retrying in {delay} seconds (attem`pt {retry_count}).")
            raise self.retry(countdown=delay)
        except self.MaxRetriesExceededError:
            # Add your notification or logging here
            print(f"ERROR: Batch {batch_id} did not complete after max retries! Manual intervention required.")
            # Optionally, send an email, Slack message, or create a ticket here
            return
