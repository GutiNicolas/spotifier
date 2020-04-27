from src.main.utils.loggerUtils import LOGGER
from src.main.connectors.youtubeConnector import youtube_connector
from src.main.impl.converter import converter_impl
from src.main.utils.stringUtils import StringUtils


def load_menu():
    logger.info("Displaying menu")
    wanna_stay = True
    while wanna_stay:
        print("-- [ Spotifier Main Menu ]  --")
        print("[ 1 ] YouTube to Spotify")
        print("[ 2 ] Spotify to YouTube")
        print("[ ANY ] Exit")
        option = input()
        if option == '1':
            print("Please paste you YouTube playlist link now")
            playlist_link = input()
            if StringUtils.is_empty(playlist_link):
                logger.info("Playlist link cannot be empty, try again")
                continue
            logger.info("YouTube to Spotify requested for playlist {}".format(playlist_link))
            converter.convert_to_spotify(playlist_link)
        if option == '2':
            print("Please paste you Spotify playlist link now")
            playlist_link = input()
            if StringUtils.is_empty(playlist_link):
                logger.info("Playlist link cannot be empty, try again")
                continue
            logger.info("Spotify to YouTube requested for playlist {}".format(playlist_link))
            converter.convert_to_youtube(playlist_link)
        else:
            wanna_stay = False
            logger.info("Terminating SPOTIFIER")
            logger.info("Bye bye")

class console_controller:

    def init(self, path):
        global logger
        global converter
        logger = LOGGER.getLogger(__name__)
        logger.info("Starting")
        converter = converter_impl(path)
        logger.info("Started")
        load_menu()
