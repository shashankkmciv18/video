import requests
import os

from dotenv import load_dotenv


class InstagramUploaderUtils:
    def __init__(self):
        load_dotenv()
        self.ig_id = os.environ.get("IG_ID")
        self.graph_api_url = os.environ.get("INSTAGRAM_GRAPH_API_URL")
        self.publish_url = os.environ.get("PUBLISH_URL")

    def upload_to_instagram(self, video_url: str, caption: str, access_token: str) -> dict:
        """
        Uploads a video to Instagram as a Reel.

        Args:
            video_url (str): The URL of the video to upload.
            caption (str): The caption for the Reel.
            access_token (str): The access token for Instagram Graph API.

        Returns:
            dict: The response from the Instagram Graph API.
        """
        url = self.graph_api_url.replace("{{IG_ID}}", self.ig_id)
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
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

    def publish_to_instagram(self, access_token: str, creation_id: str) -> dict:
        """
        Publishes a video to Instagram.

        Args:
            access_token (str): The access token for Instagram Graph API.
            creation_id (str): The creation ID of the video to publish.

        Returns:
            dict: The response from the Instagram Graph API.
        """
        url = self.publish_url.replace("{{IG_ID}}", self.ig_id)
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "creation_id": creation_id,
            "access_token": access_token
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            raise Exception(f"Request failed: {e}")


