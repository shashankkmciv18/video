import os
import uuid
import subprocess
import requests

FONT_PATH = os.path.abspath(os.path.join(os.getcwd(), "resources/Roboto-Medium.ttf"))
BACKGROUND_PATH = os.path.abspath(os.path.join(os.getcwd(), "resources/image/bg.png"))
TRANSPARENT_BACKGROUND_PATH = os.path.abspath(os.path.join(os.getcwd(), "resources/image/transparent_bg.png"))


def download_audio(url, output_path):
    resp = requests.get(url)
    with open(output_path, "wb") as f:
        f.write(resp.content)


def get_audio_duration(audio_path):
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ], stdout=subprocess.PIPE, text=True)
    return float(result.stdout.strip())


def chunk_text(text, max_words=5):
    words = text.split()
    return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]


def generate_drawtext_filters(chunks, duration, font_path, start_y=400, line_spacing=80):
    chunk_duration = (duration * 0.95) / len(chunks)
    filter_lines = []
    for i, chunk in enumerate(chunks):
        safe_chunk = chunk.replace("'", "\\'")
        start = round(i * chunk_duration, 2)
        end = round((i + 1) * chunk_duration, 2)
        y = start_y
        filter_lines.append(
            f"drawtext=fontfile='{font_path}':text='{safe_chunk}':"
            f"fontcolor=white:fontsize=60:x=(w-text_w)/2:y={y}:"
            f"enable='between(t,{start},{end})'"
        )
    return filter_lines


def merge_videos(video_paths, output_path):
    import tempfile

    # Step 1: Create a temporary list file for FFmpeg
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt") as list_file:
        for path in video_paths:
            # Important: escape single quotes and use absolute paths
            list_file.write(f"file '{os.path.abspath(path)}'\n")
        list_file_path = list_file.name

    # Step 2: Run FFmpeg to concatenate the videos
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file_path,
        "-c", "copy",
        output_path
    ]

    subprocess.run(cmd, check=True)

    # Optional: Clean up list file
    os.remove(list_file_path)


def get_ffmpeg_encoding_params(output_format: str):
    """
    Returns FFmpeg codec and pixel format parameters based on the output format.
    """
    output_format = output_format.lower()

    if output_format == "mp4":
        return [
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac"
        ]
    elif output_format == "mkv":
        return [
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac"  # You can also use "copy" if passthrough is fine
        ]
    elif output_format == "webm":
        return [
            "-c:v", "libvpx-vp9",
            "-pix_fmt", "yuv420p",
            "-c:a", "libopus"
        ]
    elif output_format == "mov":
        return [
            "-c:v", "prores_ks",
            "-pix_fmt", "yuva444p10le",  # preserves alpha
            "-c:a", "aac"
        ]
    else:
        raise ValueError(f"Unsupported format: {output_format}")


def get_output_format(output_path: str):
    """
    Returns the output format based on the file extension.
    """
    _, ext = os.path.splitext(output_path)
    ext = ext.lower()
    if ext in [".mp4", ".mkv", ".webm", ".mov"]:
        return ext[1:]


def generate_waveform(audio_path, output_path, resolution="1920x120", duration=5.0, waveform_color="white@0.7"):
    background_color = "pink"
    video_format = get_output_format(output_path)
    encoding_pattern = get_ffmpeg_encoding_params(video_format)
    command = [
        "ffmpeg", "-y",
        "-i", audio_path,

        # 👇 Create a solid blue background instead of transparent
        "-f", "lavfi", "-t", str(duration),
        "-i", f"color=color={background_color}:s={resolution}:d={duration}",

        "-filter_complex",
        f"[0:a]showwaves=s={resolution}:mode=sline:colors={waveform_color}[wave]",
        *encoding_pattern,
        "-t", str(duration),
        output_path
    ]
    subprocess.run(command, check=True)


def generate_waveform_with_image_bg(audio_path, background_image, output_path, resolution="1920x720", duration=5.0,
                                    waveform_color="white@1.0"):

    video_format = get_output_format(output_path)
    encoding_pattern =  get_ffmpeg_encoding_params(video_format)

    filter_chain = [
        f"[1:v]scale={resolution},format=rgba,colorchannelmixer=aa=0.5[bg]",  # Transparent background image
        f"[0:a]showwaves=s={resolution}:mode=line:colors={waveform_color}:scale=sqrt,format=yuva420p[wave]",
        f"[bg][wave]overlay=format=auto[out]"
    ]
    # filter_chain = [
    #     "[0:a]showwaves=colors=0xff1646@0.3:scale=sqrt:mode=cline,format=yuva420p[v]",
    #     "[1:v]scale=19200:400[bg]",
    #     "[bg][v]overlay=(W-w)/2:(H-h)/2[out]"
    # ]

    filter_complex = ";".join(filter_chain)

    command = [
        "ffmpeg", "-y",
        "-i", audio_path,  # Input audio
        "-i", background_image,  # Background image
        "-filter_complex", filter_complex,
        "-map", "[out]", "-map", "0:a",
        *encoding_pattern,
        "-t", str(duration),
        output_path
    ]
    subprocess.run(command, check=True)


def compose_video(background_path, waveform_path, audio_path, speaker, subtitle_text, duration, output_path):
    chunks = chunk_text(subtitle_text)
    subtitle_drawtexts = generate_drawtext_filters(chunks, duration, FONT_PATH)

    video_format = get_output_format(output_path)
    encoding_pattern = get_ffmpeg_encoding_params(video_format)

    # Start building the filter chain
    # filter_chain = [
    #     f"[0:v]scale=1920:1080[bg_scaled]",
    #     f"[bg_scaled][1:v]overlay=x=(W-w)/2:y=650:format=auto[bg_wave]",
    #     f"[bg_wave]drawtext=fontfile='{FONT_PATH}':text='{speaker}':fontcolor=white:fontsize=72:x=200:y=200[label_stage]"
    # ]
    filter_chain = [
        f"[0:v]scale=1920:1080[bg_scaled]",
        f"[1:v]scale=800:60[wave_scaled]",
        f"[bg_scaled][wave_scaled]overlay=x=600:y=600:format=auto[bg_wave]",
        f"[bg_wave]drawtext=fontfile='{FONT_PATH}':text='{speaker}':fontcolor=white:fontsize=72:x=200:y=200[label_stage]"
    ]

    # Chain all subtitle chunks
    current_label = "label_stage"
    for i, filter_text in enumerate(subtitle_drawtexts):
        next_label = f"sub{i}"
        filter_chain.append(f"[{current_label}]{filter_text}[{next_label}]")
        current_label = next_label

    # Final label
    filter_chain.append(f"[{current_label}]copy[final]")
    filter_complex = ";".join(filter_chain)

    # Compose the command
    command = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duration), "-i", background_path,
        "-i", waveform_path,
        "-i", audio_path,
        "-filter_complex", filter_complex,
        "-map", "[final]", "-map", "2:a",
        *encoding_pattern,
        "-shortest",

        output_path
    ]

    subprocess.run(command, check=True)


def helper(event_data: dict):
    entries = event_data["entries"]
    cdn_host = event_data["cdn_host"]
    output_dir = event_data["output_path"]
    os.makedirs(output_dir, exist_ok=True)
    video_format = '.mov'
    output_videos = []

    for entry in sorted(entries, key=lambda x: x['seq_id']):
        if entry["status"] != "complete_success":
            continue

        audio_url = f"{cdn_host}{entry['voice_url']}"
        audio_path = os.path.join(output_dir, f"{uuid.uuid4()}.wav")
        waveform_path = os.path.join(output_dir, f"{uuid.uuid4()}_wave{video_format}")
        final_output_path = os.path.join(output_dir, f"final_{uuid.uuid4()}{video_format}")

        try:
            download_audio(audio_url, audio_path)
            duration = get_audio_duration(audio_path)
            generate_waveform_with_image_bg(audio_path, TRANSPARENT_BACKGROUND_PATH, waveform_path, duration=duration)

            compose_video(
                background_path=BACKGROUND_PATH,
                waveform_path=waveform_path,
                audio_path=audio_path,
                speaker='S1',
                subtitle_text=entry["text"],
                duration=duration,
                output_path=final_output_path
            )

            output_videos.append(final_output_path)

        except Exception as e:
            print(f"Error processing {audio_url}: {e}")
            continue

    if not output_videos:
        raise ValueError("No videos were successfully generated.")

    final_merged_path = os.path.join(event_data["output_path"], f"final_merged_video{uuid.uuid4()}{video_format}")
    merge_videos(output_videos, final_merged_path)

    return final_merged_path
