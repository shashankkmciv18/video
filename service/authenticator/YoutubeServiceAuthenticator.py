import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from config.paths import TOKEN_PICKLE_FILE, SECRETS_DIR, CLIENT_SECRETS_FILE

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = TOKEN_PICKLE_FILE
SECRETS_FILE = CLIENT_SECRETS_FILE


def get_authenticated_service():
    creds = None

    # Load existing credentials
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)
    else:
        print("Token file not found. Please authenticate first.")

    # If no valid credentials, refresh or re-auth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing token...")
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for next time
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    # Return authorized YouTube API client
    return build("youtube", "v3", credentials=creds)
