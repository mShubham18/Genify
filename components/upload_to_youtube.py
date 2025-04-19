import os
import requests
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Get credentials from .env
CLIENT_ID = os.getenv("YT_CLIENT_ID")
CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")
TOKEN_URI = "https://oauth2.googleapis.com/token"

# Function to get a new access token using the refresh token
def get_access_token():
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    response = requests.post(TOKEN_URI, data=data)
    token_info = response.json()
    
    if "access_token" in token_info:
        return token_info["access_token"]
    else:
        raise Exception(f"Failed to get access token: {token_info}")

# Authenticate with YouTube API
def authenticate_youtube():
    access_token = get_access_token()
    credentials = google.oauth2.credentials.Credentials(
        access_token,
        refresh_token=REFRESH_TOKEN,
        token_uri=TOKEN_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    return build("youtube", "v3", credentials=credentials)

# Upload video function
def upload_video(video_path, title, description, tags, privacy_status="private"):
    youtube = authenticate_youtube()

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "24",  # 24 = Entertainment
        },
        "status": {
            "privacyStatus": privacy_status,  # Set to 'private' by default
        },
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()
    print("✅ Video uploaded successfully:", response)

