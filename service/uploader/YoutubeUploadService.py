import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config.paths import CLIENT_SECRETS_FILE
from service.authenticator.YoutubeServiceAuthenticator import get_authenticated_service

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def generate_token():
    secrets_path = os.path.abspath("secrets/client_secrets.json")
    flow = InstalledAppFlow.from_client_secrets_file(secrets_path, SCOPES)

    creds = flow.run_local_server(port=0)

    token_path = os.path.abspath("secrets/token.json")
    with open(token_path, "w") as token_file:
        token_file.write(creds.to_json())

    print(f"✅ Token saved at: {token_path}")


def upload_to_youtube(title: str, description: str, filePath: str) -> str:
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"Video file not found: {filePath}")
    # Save file temporarily

    try:
        # Authorize YouTube API
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

        project_path = os.path.abspath(os.path.dirname(__file__))  # adjust if needed
        # secrets = os.path.abspath(os.path.join(project_path, 'client_secrets.json'))
        secrets = CLIENT_SECRETS_FILE

        # secrets = os.path.join(project_path, "secrets/client_secrets.json")
        print(f"Using client secrets file: {secrets}")
        flow = InstalledAppFlow.from_client_secrets_file(secrets, SCOPES)
        credentials = flow.run_local_server(port=0)
        youtube = build("youtube", "v3", credentials=credentials)

        # Upload video
        request_body = {
            "snippet": {"title": title, "description": description, "categoryId": "22"},
            "status": {"privacyStatus": "private"},
        }
        media = MediaFileUpload(filePath, resumable=True)
        request_upload = youtube.videos().insert(
            part="snippet,status", body=request_body, media_body=media
        )

        response = None
        while response is None:
            status, response = request_upload.next_chunk()

        return response["id"]
    finally:
        print('file found, uploading...')


def fetchFile():
    # Fetch the file from S3 or any other source
    # For demonstration, we will use a local file
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/video/short_video.mp4"))
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Video file not found: {file_path}")
    return file_path


def default_youtube_upload():
    title = os.getenv("VIDEO_TITLE", "Daily Shorts")
    description = os.getenv("VIDEO_DESCRIPTION", "Follow for more such videos")
    tags = os.getenv("VIDEO_TAGS", "motivations,daily motivation,shorts").split(",")  # Split by comma to create a list
    video_id = upload_to_youtube_v2(
        title=title,
        description=description,
        tags=tags
    )
    return video_id
def upload_to_youtube_v2(title: str, description: str, tags: list[str]) -> str:
    file_path = fetchFile()
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Video file not found: {file_path}")

    youtube = get_authenticated_service()

    request_body = {
        "snippet": {"title": title, "description": description, "categoryId": "22"},
        "status": {"privacyStatus": "public", "madeForKids": False},
    }
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": "22",
            "tags": tags,
            "playlistId": "PLbzUSCGPJ9CCDdvtC9nYN3Pz8suCueTKg",

        },
        "status": {
            "privacyStatus": "public",
            "madeForKids": False,
            "ageRestriction": "none"
        },
    }

    media = MediaFileUpload(file_path, resumable=True)
    request_upload = youtube.videos().insert(
        part="snippet,status", body=request_body, media_body=media
    )

    print("Uploading...")
    response = None
    while response is None:
        status, response = request_upload.next_chunk()

    print(f"Upload successful: Video ID = {response['id']}")
    return response["id"]
