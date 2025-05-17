import os
import uuid
import json
import tempfile
import subprocess
import requests
from moviepy import AudioFileClip, ImageClip, TextClip, CompositeVideoClip, VideoFileClip, vfx
import cv2
from moviepy.video.fx import Resize
from moviepy.video.fx import HeadBlur


def download_audio(full_url, dest_path):
    """Download audio file from CDN"""
    response = requests.get(full_url, stream=True, timeout=(5, 15))
    response.raise_for_status()
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def generate_waveform(audio_path, output_path):
    command = [
        'ffmpeg', '-y', '-i', audio_path,
        '-filter_complex', '[0:a]showwaves=s=1280x120:mode=line:colors=white[v]',
        '-map', '[v]',
        '-pix_fmt', 'yuv420p',
        output_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print("FFmpeg error:", result.stderr)
        raise RuntimeError("FFmpeg failed to generate waveform")


def blur_image(image, ksize=25):
    return cv2.GaussianBlur(image, (ksize, ksize), 0)


def get_background(duration):
    image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/image/bg.jpg"))

    # Create the clip with duration set directly in constructor
    clip = ImageClip(image_path, duration=duration)

    # Apply Resize using the effect class
    resized_clip = clip.with_effects([Resize(new_size=(1920, 1080))])
    #
    # # Optional: Apply a basic blur (if you really need blur, and no custom blur class is available)
    # blurred_clip = resized_clip.with_effects([
    #     HeadBlur(
    #         fx=lambda t: 0.5,  # 50% from left
    #         fy=lambda t: 0.5,  # 50% from top
    #         radius=30  # blur radius in pixels
    #     )
    # ])

    return resized_clip


def get_speaker_label(name, duration, align_x=300, caption_y=520, caption_padding=200, label_offset_y=90):
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/arial.ttf"))
    label_y = caption_y - label_offset_y
    label_position = (align_x, label_y)

    clip = TextClip(font=font_path, text='S1', font_size=72, color=(255, 255, 0))
    clip = clip.with_position(label_position).with_duration(duration)
    return clip


def get_subtitle(text, duration):
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/arial.ttf"))
    return TextClip(font=font_path, text=text, font_size=48, color=(255, 255, 240)).with_position(
        ("center", "bottom")).with_duration(duration)


def get_waveform_clip(path, duration):
    return VideoFileClip(path).with_duration(duration).with_position(("center", 720))


def get_subtitle_chunks(text, duration, max_words=5, padding_bottom=200):
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/arial.ttf"))
    words = text.split()
    chunks = [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]
    chunk_duration = duration / len(chunks)

    text_clips = []
    for i, chunk in enumerate(chunks):
        clip = (
            TextClip(font=font_path, text=chunk, font_size=48, color="white", method='caption', size=(1100, None))
            .with_position(("center", 720 - padding_bottom))
            .with_start(i * chunk_duration)
            .with_duration(chunk_duration)
        )
        text_clips.append(clip)

    return text_clips



def helper(event_data: dict):
    entries = event_data["entries"]
    cdn_host = event_data["cdn_host"]
    output_dir = event_data["output_path"]
    os.makedirs(output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        sorted_entries = sorted(entries, key=lambda x: x['seq_id'])
        video_clips = []

        for idx, entry in enumerate(sorted_entries):
            if entry['status'] != 'complete_success':
                continue

            full_url = f"{cdn_host}{entry['voice_url']}"
            audio_path = os.path.join(temp_dir, f"{uuid.uuid4()}.wav")
            waveform_path = os.path.join(temp_dir, f"{uuid.uuid4()}_wave.mp4")

            try:
                # Download audio and generate waveform
                download_audio(full_url, audio_path)
                generate_waveform(audio_path, waveform_path)

                # Build video scene
                audio = AudioFileClip(audio_path)
                duration = audio.duration
                background = get_background(duration)
                speaker_label = get_speaker_label(entry['Speaker'], duration)
                # subtitle = get_subtitle(entry['text'], duration)
                # waveform = get_waveform_clip(waveform_path, duration)
                #
                # scene = CompositeVideoClip([background, waveform, subtitle, speaker_label]).with_audio(audio)
                # video_clips.append(scene)
                subtitle_chunks = get_subtitle_chunks(entry['text'], duration)  # list of subtitle clips
                waveform = get_waveform_clip(waveform_path, duration)

                scene = CompositeVideoClip([background, waveform, speaker_label] + subtitle_chunks).with_audio(audio)
                video_clips.append(scene)


            except Exception as e:
                print(f"Error processing {full_url}: {e}")
                continue

        if not video_clips:
            raise ValueError("No successful clips were processed.")

        # Concatenate all scenes
        from moviepy import concatenate_videoclips
        final_video = concatenate_videoclips(video_clips, method="compose")
        final_output_path = os.path.join(output_dir, f"final_video_{uuid.uuid4()}.mp4")
        final_video.write_videofile(final_output_path, fps=24,
                                    codec="libx264",
                                    audio_codec="aac",
                                    preset="ultrafast",
                                    threads=8)

    return final_output_path
