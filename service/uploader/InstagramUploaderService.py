import os
from sqlite3 import Connection

import requests
from dotenv import load_dotenv
from fastapi import Depends

from db import get_db, get_db_1
from repository.InstagramUploadRepository import InstagramRepository

load_dotenv()



class InstagramUploaderService:
    def __init__(self, repo: InstagramRepository):
        self.repo = repo

    def upload_to_instagram(self,video_url: str, caption: str, access_token: str) -> dict:
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
            if response.status_code == 200:
                return response.json()
            else:
                # Handle non-200 responses
                print(f"Error: {response.status_code} - {response.text}")
                raise Exception(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

    def publish_to_instagram(self,access_token: str, creation_id: str) -> dict:

        url = os.environ.get("PUBLISH_URL")
        IG_ID = os.environ.get("IG_ID")
        url = url.replace("{{IG_ID}}", IG_ID)
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

    def upload_video(self, video_url: str, caption: str):
        try:

            repo = self.repo
            access_token = os.getenv("USER_LONG_LIVE_TOKEN")

            response = self.upload_to_instagram(video_url, caption, access_token)
            instagram_creation_id = response.get("id")

            is_published = response.get("is_published", False)

            # Create a new entry
            repo.create_creation_entry(instagram_creation_id, is_published)
            return response
        except Exception as e:
            return {"error": str(e)}

    def publish_video(self, creation_id: str):
        try:
            repo = self.repo
            access_token = os.getenv("USER_LONG_LIVE_TOKEN")
            response = self.publish_to_instagram(access_token, creation_id)
            instagram_content_id = response.get("id")
            is_published = True
            instagram_creation_id = creation_id
            repo.update_creation_entry(instagram_creation_id, is_published, instagram_content_id)
        except Exception as e:
            return {"error": str(e)}
