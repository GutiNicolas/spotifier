from src.main.utils.loggerUtils import LOGGER
from src.main.connectors.youtubeConnector import youtube_connector
from src.main.utils.collectionUtils import CollectionUtils
from src.main.utils.stringUtils import StringUtils
from src.main.connectors.spotifyConnector import spotify_connector


class converter_impl:

    def __init__(self, path):
        global logger
        global youtube
        global spotify
        youtube = youtube_connector(path)
        spotify = spotify_connector()
        logger = LOGGER.getLogger(__name__)


    def convert_to_spotify(self, playlist):
        logger.info("Converter from YouTube to Spotify started for playlist {}".format(playlist))
        songs_list = youtube.search_from_playlist(playlist)
        if(CollectionUtils.is_empty(songs_list)):
            logger.warn("Stopping YouTube to Spotify converter. Could not get a list of songs for playlist {}".format(playlist))
            return
        songs_touples = CollectionUtils.element_to_tuple_by_separator(coll=songs_list, separator="-")
        spotify_uris = []
        for tuple in songs_touples:
            logger.info("Searching for {} by {} on Spotify".format(tuple[1], tuple[0]))
            uri = spotify.search_for_song(artist_name=tuple[0], song_name=tuple[1])
            if(StringUtils.is_empty(uri)):
                logger.warn("{} by {} not found on Spotify".format(tuple[1], tuple[0]))
                continue
            logger.info("{} by {} found on Spotify, URI for {} is [{}]".format(tuple[1], tuple[0], uri, tuple[1]))
            spotify_uris.append(uri)



