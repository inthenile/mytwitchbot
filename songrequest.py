import os.path
import pickle
from dotenv import dotenv_values
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request

config = dotenv_values(".env")
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl", "https://www.googleapis.com/auth/youtubepartner", "https://www.googleapis.com/auth/youtube"]
youtube_api_key = config["YOUTUBE_API_KEY"]
youtube_channel_id = config["YOUTUBE_CHANNEL_ID"]
client_secrets_file = ".clients_secret.json"
api_service_name = "youtube"
api_version = "v3"

credentials = None
#this creates a private playlist after authorization

#if we have saved our credentials, we load them
if os.path.exists('token.pickle'):
    print('Loading Credentials from file...')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)

#else we refresh/get new ones
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refresh token")
        credentials.refresh(Request())
    else:
        print("Fetching new tokens")
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        flow.run_local_server()
        credentials = flow.credentials
        #writing credenetials onto token.pickle for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

# creating a playlist by way of example
youtube = build(api_service_name, api_version, credentials=credentials)
request = youtube.playlists().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "Stream playlist",
            "description": "This is where songrequests will go.",

        },
        "status": {
            "privacyStatus": "private"
        }
    }
)
response = request.execute()



print(response)

