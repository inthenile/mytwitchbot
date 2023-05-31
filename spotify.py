import json
from dotenv import dotenv_values
import base64
from requests import post, put

config = dotenv_values(".env")
spotify_client_id = config["SPOTIFY_CLIENT_ID"]
spotify_client_secret = config["SPOTIFY_CLIENT_SECRET"]

def get_spotify_token():
    """retrieve the access token"""
    auth_string = (spotify_client_id + ":" + spotify_client_secret).encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_string), "utf-8")
    # url to make a POST request to
    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + auth_base64,
               "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    return json_result["access_token"]

def get_auth_header(token):
    """get the header"""
    return {"Authorization": "Bearer " + token}

def play_song(token, song_request):
    # getting the spotify uri for the song from the requested link.
    reverse_link = song_request[::-1]
    reverse_uri = reverse_link[reverse_link.index("?") + 1:reverse_link.index("/")]
    spotify_uri = reverse_uri[::-1]

    url = "https://api.spotify.com/v1/me/player/play"
    headers = get_auth_header(token)
    data = {"context_uri": "spotify:track:" + spotify_uri}
    sr = put(url=url, headers=headers, data=data)
    return sr


token = get_spotify_token()
#play_song(token, song_request="https://open.spotify.com/track/4r6bMqodL3zsAMQ44ojyjB?si=c79a82fe50844e5b")
