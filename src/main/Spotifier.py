import logging
import sys
from pathlib import Path
from src.properties import logging_properties, spotify_properties, youtube_properties
from src.main.controllers.console import console_controller


def check_properties_ok():
    if spotify_properties.username == "DEFAULT" or spotify_properties.api_key == "DEFAULT":
        logger.warning("Load your Spotify properties on properties.py and restart applicacion")
        sys.exit()

    if youtube_properties.username == "DEFAULT" or youtube_properties.api_key == "DEFAULT":
        logger.warning("Load your YouTube properties on properties.py and restart applicacion")
        sys.exit()

    logger.info("All properties are OK, initializing server")

def load_menu():
    console_controller.init(None)

def init():
    try:
        path = str(Path(__file__).parent.absolute()).replace('src/main', 'logs/{}')
        logging.basicConfig(filename=path.format(logging_properties.logging_filename), format=logging_properties.logging_template, level=logging.INFO)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(logging_properties.logging_template))
        console_handler.setLevel(logging.INFO)

        global logger
        logger = logging.getLogger('Spotifier')
        logger.addHandler(console_handler)
        logger.info("Loading SPOTIFIER")

        # check_properties_ok()

        load_menu()


    except Exception as ex:
        logger.error(ex)
        print("Exception catched")
        sys.exit()

if __name__ == "__main__":
    init()
