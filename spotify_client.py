# spotify_client.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Define the scope required for reading listening history and managing playlists.
SCOPE = "user-read-recently-played playlist-modify-public playlist-modify-private"

def get_spotify_client():
    """
    Authenticate the user and return a Spotipy client instance.
    This function uses the built-in token cache.
    """
    # Pass credentials explicitly from environment variables
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=SCOPE
    )
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        # If no token is cached, print the URL and ask user to authorize.
        auth_url = sp_oauth.get_authorize_url()
        print("Please navigate here to authorize:")
        print(auth_url)
        # After authorization, the user is redirected to the SPOTIPY_REDIRECT_URI.
        # The URL will include a code. Ask the user to paste it.
        response = input("Paste the URL you were redirected to: ")
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)
    token = token_info['access_token']
    sp = spotipy.Spotify(auth=token)
    return sp
