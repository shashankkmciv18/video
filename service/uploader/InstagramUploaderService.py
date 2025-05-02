import os

import requests
from dotenv import load_dotenv

load_dotenv()


def upload_to_instagram(video_url: str, caption: str, access_token: str) -> dict:
    """
    Uploads a video to Instagram as a Reel.

    Args:
        video_url (str): The URL of the video to upload.
        caption (str): The caption for the Reel.
        access_token (str): The access token for Instagram Graph API.

    Returns:
        dict: The response from the Instagram Graph API.
    """

    url = os.environ.get("INSTAGRAM_GRAPH_API_URL")
    IG_ID = os.environ.get("IG_ID")
    url = url.replace("{{IG_ID}}", IG_ID)
    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": "true",
        "access_token": access_token,
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}