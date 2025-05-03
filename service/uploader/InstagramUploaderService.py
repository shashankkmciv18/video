import os
import time

import requests
from dotenv import load_dotenv

from repository.InstagramUploadRepository import InstagramRepository
from service.content_generator.VideoGenerator import generate_videos_for_platforms
from service.uploader.InstagramUploaderUtils import InstagramUploaderUtils
from service.uploader.S3UploaderService import S3UploaderService

load_dotenv()



class InstagramUploaderService:

    def __init__(self, repo: InstagramRepository):
        self.repo = repo
        self.s3_uploader_service = S3UploaderService()
        self.instagram_uploader_utils = InstagramUploaderUtils()

    def upload_video(self, video_url: str, caption: str):
        try:

            repo = self.repo
            access_token = os.getenv("USER_LONG_LIVE_TOKEN")

            response = self.instagram_uploader_utils.upload_to_instagram(video_url, caption, access_token)
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
            response = self.instagram_uploader_utils.publish_to_instagram(access_token, creation_id)
            instagram_content_id = response.get("id")
            is_published = True
            instagram_creation_id = creation_id
            repo.update_creation_entry(instagram_creation_id, is_published, instagram_content_id)
            return  response
        except Exception as e:
            return {"error": str(e)}

    def generateAndPostVideo(self, caption):
        try:
            path = generate_videos_for_platforms()
        except Exception as e:
            raise Exception("Video generation failed")
        try:
            url = self.s3_uploader_service.upload_file_to_s3(file_path=path)
        except Exception as e:
            raise Exception("S3 upload failed")
        access_token = os.getenv("USER_LONG_LIVE_TOKEN")
        try:
            response = self.upload_video(url, caption)
        except Exception as e:
            raise Exception("Instagram upload failed")
        if response.get("error"):
            raise Exception("Instagram upload failed")
        # Here It video would require some time to be able to upload

        time.sleep(60)
        try:
            self.publish_video(response.get("id"))
        except Exception as e:
            raise Exception("Instagram publish failed")
        return response