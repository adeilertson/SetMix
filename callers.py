import json
import logging
import requests
from requests.exceptions import ConnectionError
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import file_handeling

module_logger = logging.getLogger("primary.callers")


def setlist_call(url):
    """Setlist.fm API call

    Args:
        url (str): URL for API call

    Returns:
        dict: JSON response data converted to dict for returned data
    """
    # Load config to get API key
    cfg = file_handeling.get_config()
    # Set headers with API key and return format
    headers = {
    'x-api-key': cfg['setlist_fm_api_key'],
    'accept': 'application/json'
    }
    # Make API call
    try:
        res = requests.get(url, headers=headers)
    except ConnectionError:
        module_logger.error(f"setlist.fm - Connection error while attempting to make call to {url}")
        print(f"\nConnection error while attempting to make call to {url}")
        cont = input('\nPress enter to return to menu.\n')
        return None
    # Convert response to json
    data = json.loads(res.content)

    # Bad result check
    # 'status' only returned with errors
    if 'status' in data.keys():
        module_logger.error(f"setlist.fm - Status {data['code']} {data['status']} returned for {url}")
        print(f"\nError - Status {data['code']} {data['status']} returned for {url}")
        cont = input('\nPress enter to return to menu.\n')
        return None

    module_logger.info(f"Succesful call to {url}")
    return data


def spotify_auth():
    # Get config
    cfg = file_handeling.get_config()
    # Login
    sp_session = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=cfg['spotify_client_id'],
            client_secret=cfg['spotify_secret'],
            redirect_uri=cfg['spotify_uri'],
            scope=cfg['spotify_scope']
            )
        )
    module_logger.info(f"spotify - OAuth completed for user {sp_session.me()['id']}")
    return sp_session

def create_playlist(sp_session, playlist_name):
    user_id = sp_session.me()['id']
    playlist = sp_session.user_playlist_create(user_id, playlist_name)
    module_logger.info(f"spotify - Created playlist {playlist_name} for user {sp_session.me()['id']}")
    return playlist
