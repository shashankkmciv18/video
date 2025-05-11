import os
import tempfile
import uuid
import subprocess
import requests


from eventHandler.celery_app import celery_app
from service.uploader.S3UploaderService import S3UploaderService


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60, name="audio_merge_task", queue="audio_queue")
def download_and_merge_audio(self, event_data: dict):
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
        upload_url = s3_uploader_service.upload_file_to_s3(file_path=path,s3_file_key= s3_file_key )
        print(f"File uploaded to S3: {upload_url}")


def helper(event_data: dict):
    entries = event_data["entries"]
    cdn_host = event_data["cdn_host"]
    output_dir = event_data["output_path"]

    os.makedirs(output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Sort entries based on seq_id to maintain order
        sorted_entries = sorted(entries, key=lambda x: x['seq_id'])

        audio_files = []  # List to store paths of downloaded audio files

        # Temporary path for silence if any pause needs to be inserted
        silence_file = os.path.join(temp_dir, "silence.wav")
        silence_duration = 1000  # 1 second of silence

        for entry in sorted_entries:
            if entry['status'] != 'complete_success':
                continue  # Skip entries that are not successful

            # Construct the full URL
            full_url = f"{cdn_host}{entry['voice_url']}"

            try:
                response = requests.get(full_url, stream= True, timeout=(5,15))
                response.raise_for_status()

                # Save the audio file temporarily
                temp_audio_path = os.path.join(temp_dir, f"{uuid.uuid4()}.wav")
                with open(temp_audio_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                # Add the audio file path to the list
                audio_files.append(temp_audio_path)

                # Handle pause if specified
                pause_duration = entry.get('pause_seconds', 0)
                if pause_duration > 0:
                    pause_path = os.path.join(temp_dir, f"silence_{uuid.uuid4()}.wav")
                    silence_cmd = [
                        "ffmpeg", "-f", "lavfi", "-t", str(pause_duration/10),
                        "-i", "anullsrc=r=44100:cl=stereo", pause_path
                    ]
                    subprocess.run(silence_cmd, check=True)
                    audio_files.append(pause_path)

            except Exception as e:
                print(f"Error processing {full_url}: {e}")
                continue

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Generate a unique filename for the merged audio
        output_filename = f"merged_{uuid.uuid4()}.wav"
        output_path = os.path.join(output_dir, output_filename)

        # Use FFmpeg to merge the audio files
        concat_file = os.path.join(temp_dir, "concat_list.txt")

        with open(concat_file, 'w') as f:
            for audio_file in audio_files:
                f.write(f"file '{audio_file.replace("'", "'\\''")}'\n")


        # Use FFmpeg to merge all audio files in the list
        ffmpeg_cmd = f"ffmpeg -f concat -safe 0 -i {concat_file} -c copy {output_path}"
        subprocess.run(ffmpeg_cmd, shell=True, check=True)

    return output_path
