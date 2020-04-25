import json

from src.main.utils.collectionUtils import CollectionUtils
from src.main.utils.stringUtils import StringUtils
from src.properties import spotify_properties
import requests
from src.main.utils.loggerUtils import LOGGER

SPOTIFY_NEW_PLAYLIST_ENDPOINT = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_properties.client_id)
SPOTIFY_SONG_QUERY_ENDPOINT = "https://api.spotify.com/v1/search?q={}%20{}&type=track&offset=0&limit=20"

DEFAULT_HEADERS = {"Content-Type":"application/json", "Authorization":"Bearer {}".format(spotify_properties.client_secret)}

class spotify_connector:

    def __init__(self):
        global logger
        logger = LOGGER.getLogger(__name__)
        logger.info("Initialaizing Spotify connector")

    def get_spotify_auth_token(self):
        requests.get("https://accounts.spotify.com/authorize?response_type=code&client_id={}&scope=user-read-private%20user-read-email%20playlist-modify-private%20playlist-modify-public")

    def get_spotify_uri(self):
        pass

    def add_song_to_playlist(self):
        pass

    # Creates a HTTP.POST request aiming to create a new playlist
    #
    # returns the created playlist ID
    def create_spotify_playlist(self, name, description, public):
        body = json.dumps({"name":name, "description":description, "public":public})
        logger.info("Sending Create Playlist post request to Spotify. Data = {}".format(body))
        r = requests.post(SPOTIFY_NEW_PLAYLIST_ENDPOINT, data=body, headers=DEFAULT_HEADERS)
        logger.info("Spotify responded with a status code {} and data {}".format(r.status_code, r.json()))
        r_json = r.json()
        print(r_json)

        return r_json["id"]

    def search_for_song(self, artist_name, song_name):
        query = SPOTIFY_SONG_QUERY_ENDPOINT.format(artist_name, StringUtils.clean_queriable(song_name))
        logger.info("[SFS] Sending Search Song get request to Spotify. Query is [{}]".format(query))
        print(DEFAULT_HEADERS)
        r = requests.get(query, headers=DEFAULT_HEADERS)
        logger.info("[SFS] Spotify responded with a status code {}".format(r.status_code))
        r_json = r.json()
        print(r_json)

        uri = None
        if ( r_json is not None and CollectionUtils.none_empty(r_json['tracks']['items'])):
            songs = r_json["tracks"]["items"]
            uri = songs[0]["uri"]
            logger.info("[SFS] Founded URI for Song {} is [{}]".format(song_name, uri))
        return uri
