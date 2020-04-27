from src.main.utils import variablesCatalog
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

    def get_playlist_inputs(self):
        global playlist_name
        global playlist_public
        print("Name for your new Playlist:")
        playlist_name = input()
        print("Description for your new Playlist (Optional, leave it empty if dont wanna have one):")
        playlist_desc = input()
        print("Would you like your playlist to be Public?:  Y/N")
        playlist_public = input()

        friction_counter = 0
        while playlist_public != 'Y' and playlist_public != 'N' and friction_counter < 3:
            friction_counter += 1
            print(friction_counter)
            if (friction_counter == 2):
                print("Warning, last chance or will use default value")
            print("Would you like your playlist to be Public?: Please reply with  Y/N")
            playlist_public = input()

        if (playlist_public != 'Y' and playlist_public != 'N'):
            playlist_public = 'Y'

        is_public = playlist_public == 'Y'

        if StringUtils.is_empty(playlist_name):
            print("Your new playlist name CANNOT BE EMPTY, Pleas provide one:")
            playlist_name = input()

        if StringUtils.is_empty(playlist_name):
            print("Playlist name not provided, would you like to abort converse operation?:  Y/N")
            wanna_quit = input()
            while wanna_quit is not 'Y' or 'N':
                print("Please reply with  Y/N")
                wanna_quit = input()

            if wanna_quit == 'Y':
                print('Stopping operation')
                logger.warn('Stopping playlist conversion operation')
                return None

            print("Your new playlist name CANNOT BE EMPTY, Pleas provide one:")
            playlist_name = input()

        if StringUtils.is_empty(playlist_name):
            print('Stopping operation, no name was provided')
            logger.warn('Stopping playlist conversion operation, Reason: No name provided')
            return None

        return {variablesCatalog.playlist_name:playlist_name, variablesCatalog.playlist_desc:playlist_desc, variablesCatalog.playlist_public:is_public}


    def convert_to_spotify(self, playlist):
        logger.info("Converter from YouTube to Spotify started for playlist {}".format(playlist))
        songs_list = youtube.search_from_playlist(playlist)
        if(CollectionUtils.is_empty(songs_list)):
            logger.warn("Stopping YouTube to Spotify converter. Could not get a list of songs for playlist {}".format(playlist))
            return
        songs_touples = CollectionUtils.element_to_tuple_by_separator(coll=songs_list, separator="-")
        print("SONGS {}".format(songs_touples))
        spotify_uris = []
        not_found_songs = []
        for tuple in songs_touples:
            logger.info("Searching for {} by {} on Spotify".format(tuple[1], tuple[0]))
            uri = spotify.search_for_song(artist_name=tuple[0], song_name=tuple[1])
            if(StringUtils.is_empty(uri)):
                logger.warn("{} by {} not found on Spotify".format(tuple[1], tuple[0]))
                not_found_songs.append((tuple[1], tuple[0]))
                continue
            logger.info("{} by {} found on Spotify, URI for {} is [{}]".format(tuple[1], tuple[0], tuple[1], uri))
            spotify_uris.append(uri)

        logger.info("Dot found the following songs on Spotify: {}".format(not_found_songs))
        for tuple in not_found_songs:
            logger.info("Now Searching for {} by {} on Spotify, Best luck!".format(tuple[1], tuple[0]))
            uri = spotify.search_for_song(artist_name=tuple[0], song_name=tuple[1])
            if(StringUtils.is_empty(uri)):
                logger.warn("{} by {} not found on Spotify. We dont have more options than skipping it. :( Sorry!".format(tuple[1], tuple[0]))
                continue
            logger.info("{} by {} finally found on Spotify, Cheers!, URI for {} is [{}]".format(tuple[1], tuple[0], tuple[1], uri))
            spotify_uris.append(uri)

        logger.info("Final URI list is {}".format(spotify_uris))

        playlist_input = self.get_playlist_inputs()

        if playlist_input is not None:
            spotify_playlist_id = spotify.create_spotify_playlist(playlist_input[variablesCatalog.playlist_name], playlist_input[variablesCatalog.playlist_desc], playlist_input[variablesCatalog.playlist_public])

            if spotify_playlist_id is not None:
                spotify.add_song_to_playlist(spotify_playlist_id, spotify_uris)

            logger.info("Finished YouTube to Spotify conversion, check your new playlist: https://open.spotify.com/playlist/{}".format(spotify_playlist_id))


    def convert_to_youtube(self, playlist):
        logger.info("Converter from Spotify to YouTube started for playlist {}".format(playlist))
        songs_touples = spotify.search_from_playlist(playlist)

        print("SONGS {}".format(songs_touples))
        youtube_ids = []
        not_found_songs = []
        for tuple in songs_touples:
            logger.info("Searching for {} by {} on YouTube".format(tuple[1], tuple[0]))
            id = youtube.find_song_on_youtube(tuple[0], tuple[1])
            if (StringUtils.is_empty(id)):
                logger.warn("{} by {} not found on YouTube".format(tuple[1], tuple[0]))
                not_found_songs.append((tuple[1], tuple[0]))
                continue
            logger.info("{} by {} found on YouTube, ID for {} is [{}]".format(tuple[1], tuple[0], tuple[1], id))
            youtube_ids.append(id)

        logger.info("Dot found the following songs on Spotify: {}".format(not_found_songs))

        for tuple in not_found_songs:
            logger.info("Now Searching for {} by {} on Spotify, Best luck!".format(tuple[1], tuple[0]))
            id = youtube.find_song_on_youtube(artist_name=tuple[0], song_name=tuple[1])
            if(StringUtils.is_empty(id)):
                logger.warn("{} by {} not found on Spotify. We dont have more options than skipping it. :( Sorry!".format(tuple[1], tuple[0]))
                continue
            logger.info("{} by {} finally found on Spotify, Cheers!, URI for {} is [{}]".format(tuple[1], tuple[0], tuple[1], id))
            youtube_ids.append(id)

        logger.info("Final IDs list is {}".format(youtube_ids))

        playlist_input = self.get_playlist_inputs()

        if playlist_input is not None:
            playlist_privacy_level = "public" if playlist_input[variablesCatalog.playlist_public] else "private"
            youtube_playlist_id = youtube.create_youtube_playlist(playlist_input[variablesCatalog.playlist_name], playlist_input[variablesCatalog.playlist_desc], playlist_privacy_level)

            if youtube_playlist_id is not None:
                youtube.add_all_to_playlist(youtube_ids, youtube_playlist_id)

            logger.info("Finished YouTube to Spotify conversion, check your new playlist: https://www.youtube.com/playlist?list={}".format(youtube_playlist_id))
