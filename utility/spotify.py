import base64
import json
import secrets
import string
import sys
import webbrowser
from dotenv import dotenv_values
import requests

config = dotenv_values(".env")

spotify_client_id = config["SPOTIFY_CLIENT_ID"]
spotify_client_secret = config["SPOTIFY_CLIENT_SECRET"]
spotify_redirect_uri = config["SPOTIFY_REDIRECT_URI"]

credential_bytes = (spotify_client_id + ":" + spotify_client_secret).encode("utf-8")
b64_bytes = base64.urlsafe_b64encode(credential_bytes)
b64_credentials = b64_bytes.decode("utf-8")


is_spotify_active = input("Do you want to use Spotify? 'y'/'n'?")
if is_spotify_active.lower() == 'n':
    print("You can restart the bot if you change your decision.")
else:
    def authorise_user():
        base_url = "https://accounts.spotify.com/authorize?"
        response_type = "code"
        client_id = spotify_client_id
        scope = "user-modify-playback-state user-read-playback-state user-read-currently-playing"
        redirect_uri = spotify_redirect_uri
        state = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        request_link = requests.get(base_url, params={"base_url":  base_url, "response_type": response_type, "client_id": client_id,
                                                      "scope": scope, "redirect_uri": redirect_uri, "state": state})

        webbrowser.open(request_link.url)
        callback_url = input("Enter the url you got here:")
        try:
            response = callback_url.split("?")[1].split("&")
            response_code_unsplit = response[0]
            response_code = response_code_unsplit.split("=")[1]
            response_state_unsplit = response[1]
            response_state = response_state_unsplit.split("=")[1]

            if response_state != state:
                print("You were not authenticated.")
                sys.exit(0)
            else:
                print("You are successfully authenticated.")
                return response_code

        except Exception:
            print("There was a problem. Restart the bot if you wish to retry authentication. ")

    response_code = authorise_user()

    def get_access_token():
        base_url = "https://accounts.spotify.com/api/token"
        form = {"grant_type": "authorization_code",
                "code": response_code,
                "redirect_uri": spotify_redirect_uri}
        headers = {"Authorization": "Basic " + str(b64_credentials),
                   "content_type": "application/x-www-form-urlencoded"}

        p_request = requests.post(base_url, data=form, headers=headers)
        response = json.loads(p_request.content)
        return response

    token = get_access_token()

    access_token = token["access_token"]
    refresh_token = token["refresh_token"]

    async def refresh_access_token():

        base_url = "https://accounts.spotify.com/api/token"
        form = {"grant_type": "refresh_token",
                "refresh_token": refresh_token}
        headers = {"Authorization": "Basic " + str(b64_credentials),
                   "content_type": "application/x-www-form-urlencoded"}

        requests.post(base_url, data=form, headers=headers)

    async def get_playing_song():
        try:
            base_url = "https://api.spotify.com/v1/me/player/currently-playing"
            headers = {"Authorization": "Bearer " + access_token}
            p_request = requests.get(base_url, headers=headers)
            response = json.loads(p_request.content)
            return response
        except Exception:
            return "Something went wrong"

