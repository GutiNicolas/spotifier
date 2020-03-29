from src.main.utils.loggerUtils import LOGGER
from src.main.connectors.youtubeConnector import youtube_connector


def load_menu():
    logger.info("Displaying menu")
    wanna_stay = True
    while wanna_stay:
        print("-- [ Spotifier Main Menu ]  --")
        print("[ 1 ] YouTube to Spotify")
        print("[ 9 ] List YouTube Playlists Songs")
        print("[ ANY ] Exit")
        option = input()
        if option == '1':
            print("Please paste you Spotify playlist link now")
            playlist_link = input()
            logger.info("YouTube to Spotify requested for playlist {}".format(playlist_link))
        if option == '9':
            print("Please paste you YouTube Playlist link now")
            playlist_link = input()
            logger.info("YouTube search for playlist {}".format(playlist_link))
            youtube.search_from_playlist(url=playlist_link)

        else:
            wanna_stay = False
            logger.info("Terminating SPOTIFIER")
            logger.info("Bye bye")
class console_controller:

    def init(self, path):
        global logger
        global youtube
        youtube = youtube_connector(path)
        logger = LOGGER.getLogger(__name__)
        logger.info("Started")
        load_menu()
