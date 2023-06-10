import os.path
import pickle
from dotenv import dotenv_values
from googleapiclient.discovery import build
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request


config = dotenv_values(".env")
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl", "https://www.googleapis.com/auth/youtubepartner",
          "https://www.googleapis.com/auth/youtube"]
youtube_api_key = config["YOUTUBE_API_KEY"]
youtube_channel_id = config["YOUTUBE_CHANNEL_ID"]
client_secrets_file = ".clients_secret.json"
api_service_name = "youtube"
api_version = "v3"

credentials = None
playlist_id = None

# this creates a private playlist after authorization or loads it if we saved a previous playlist id

# if we have saved our credentials, we load them
if os.path.exists('token.pickle'):
    print('Loading Credentials from file...')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)
# creating a playlist by way of example

# else we refresh/get new ones / which also means we should have no dedicated playlist, so we create one and grab its ID
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refreshing token")
        credentials.refresh(Request())
    else:
        print("Fetching new tokens")
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        flow.run_local_server()
        credentials = flow.credentials
        # writing credentials onto token.pickle for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    youtube = build(api_service_name, api_version, credentials=credentials)

class Playlist:
    def __init__(self, pl_id):
        self.pl_id = pl_id

    async def make_playlist(self):
        # check if you already have a playlist saved
        if os.path.exists("playlist.txt"):
            print("You already have a playlist ready to go")
            with open("playlist.txt", "r") as file:
                self.pl_id = file.readline()
                return self.pl_id
        else:
            request = youtube.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": "Stream playlist",
                        "description": "This is where song requests will go.",
                    },
                    "status": {
                        "privacyStatus": "private"
                    }
                }
            )
            response = request.execute()
            self.pl_id = response["id"]
            with open("playlist.txt", "w") as file:
                file.write(str(self.pl_id))
            return self.pl_id

async def song_request(playlistId, videoId):
    from urllib.parse import urlparse
    parsed_id = urlparse(videoId)
    parsed_link = None
    if parsed_id.netloc == "www.youtube.com":
        parsed_link = parsed_id.query[2:]
    elif parsed_id.netloc == "youtu.be":
        parsed_link = parsed_id.path[1:]
    else:
        print("Bad link.")

    add_to_playlist = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": f"{playlistId}",
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": f"{parsed_link}"
                }
            }
        }
    )
    add_to_playlist.execute()
    print("Song successfully added to playlist.")


