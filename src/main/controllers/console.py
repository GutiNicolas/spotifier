from src.main.utils.loggerUtils import LOGGER


def load_menu():
    logger.info("Displaying menu")
    wanna_stay = True
    while wanna_stay:
        print("-- [ Spotifier Main Menu ]  --")
        print("[ 1 ] Spotify to YouTube")
        print("[ ANY ] Exit")
        option = input()
        if option == '1':
            print("Please paste you Spotify playlist link now")
            playlist_link = input()
            logger.info("Spotify to YouTube requested for playlist {}".format(playlist_link))
        else:
            wanna_stay = False
            logger.info("Terminating SPOTIFIER")
            logger.info("Bye bye")
class console_controller:

    def init(self):
        global logger
        logger = LOGGER.getLogger(__name__)
        logger.info("Started")
        load_menu()
