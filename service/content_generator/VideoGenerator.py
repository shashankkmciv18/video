import time

import requests

from moviepy.video.VideoClip import ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
import logging

from service.content_generator.ImageGenerator import fetch_background_image
from service.content_generator.ImageHelper import overlay_text_on_image_vertical
from service.sentiment_analyser.SentimentAnalyser import do_sentiment_analysis



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)



def fetch_quote():
    # Uncomment the following lines to fetch a random quote from ZenQuotes API
    response = requests.get("https://zenquotes.io/api/random")
    quote_data = response.json()
    quote = quote_data[0]['q']  # 'q' is the quote, 'a' is the author
    return quote


# Fetch a motivational quote from ZenQuotes API
def fetch_motivational_quote():
    # Uncomment the following lines to fetch a random quote from ZenQuotes API
    too_many_requests_response = 'Too many requests. Obtain an auth key for unlimited access.'
    while True:
        quote = fetch_quote()
        print(quote)
        if quote == too_many_requests_response:
            logging.warning("Received 'Too many requests' response. Retrying...")
            time.sleep(45)
            continue
        if do_sentiment_analysis(quote):
            return quote

        logging.warning("Negative sentiment detected. Fetching a new quote...")
        time.sleep(15)


# Fetch a random background image from Unsplash



def create_vertical_video(output_video):
    duration = 12  # Duration of the video in seconds

    resources_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources"))
    background_image_path = os.path.join(resources_dir, 'final_background_vertical.jpg')
    clip = ImageClip(background_image_path, duration=duration)
    video_with_audio = clip

    # Optional: Add background music

    background_music_path = os.path.join(resources_dir, 'background_music.mp3')
    if os.path.exists(background_music_path):
        audio = AudioFileClip(background_music_path).subclipped(0, duration)
        video_with_audio = clip.with_audio(audio)

    # Output video

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/video"))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_name = os.path.join(output_dir, 'short_video.mp4')

    save_video(video_with_audio, file_name)
    return file_name


def save_video(video, output_path):
    video.write_videofile(output_path, fps=30, codec='libx264', audio_codec='aac')


def generate_videos_for_platforms():
    quote = fetch_motivational_quote()
    fetch_background_image()
    overlay_text_on_image_vertical(quote)

    # Generate video for YouTube Shorts
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(":", "-")
    path = create_vertical_video(f'short_video_{timestamp}.mp4')
    return path



