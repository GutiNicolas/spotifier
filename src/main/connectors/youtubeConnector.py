from src.main.utils.loggerUtils import LOGGER
import os
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import sys
import googleapiclient.errors
import requests
import youtube_dl
from src.main.utils.stringUtils import StringUtils

class youtube_connector:

    def __init__(self, path):
        global logger
        logger = LOGGER.getLogger(__name__)
        logger.info("Initialaizing YouTube connector")
        self.youtube = self.get_youtube_client(path)
        
    def create_secrent_file_and_warn(self, path):
        logger.warn("client_secrets.json not found, creating it, please fill it and restart application")
        f = open(path, "x")
        f.write("{ \n\"web\": {\n \"client_id\": \"\", \n\"client_secret\": \"\", \n\"redirect_uris\": [\"\"], \n\"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\", \n\"token_uri\": \"https://accounts.google.com/o/oauth2/token\", \n\"YOUR_API_KEY\": \"\" \n}\n}")
        sys.exit()
        
        
    # Logs into YouTube
    # from YouTube Data API Doc
    # returns a YouTube client
    def get_youtube_client(self, path):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = path.replace('main', 'client_secrets.json')

        if(not os.path.exists(client_secrets_file)):
            self.create_secrent_file_and_warn(client_secrets_file)

        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        youtube_client = build(api_service_name, api_version, credentials=credentials)

        return youtube_client

    # Retuns a list of song titles contained on a playlist
    def search_from_playlist(self, url):
        playlist_id = url.split("list=")[1].split('&')[0]
        logger.info("[SearchFromPlaylist] Using {} as Playlist ID".format(playlist_id))
        if StringUtils.is_empty(playlist_id):
            logger.warn("[SearchFromPlaylist] YouTube Playlist ID not found on url {}".format(url))
            return []
        logger.info("[SearchFromPlaylist] Requesting data for YouTube Playlist with ID {}".format(playlist_id))

        songs_list_request = self.youtube.playlistItems().list(playlistId=playlist_id, part="snippet", maxResults=50)
        songs_list_response = songs_list_request.execute()
        logger.info("[SearchFromPlaylist] Response is")
        logger.info(songs_list_response)

        songs_list = []
        if songs_list_response is not None:
            logger.info("[SearchFromPlaylist] {} found on Playlist with ID {}".format(len(songs_list_response["items"]), playlist_id))
            for song in songs_list_response["items"]:
                song_title = song["snippet"]["title"]
                logger.info("[SearchFromPlaylist] Added {}".format(song_title))
                songs_list.append(song_title)

        return songs_list
