import logging
import sys
from pathlib import Path

from src.main.connectors.spotifyConnector import spotify_connector
from src.main.utils.collectionUtils import CollectionUtils
from src.main.utils.stringUtils import StringUtils
from src.properties import logging_properties, spotify_properties, youtube_properties
from src.main.controllers.console import console_controller

playlist_songs = ['Chase Atlantic - Swim / Lyrics', 'Chase Atlantic - Slow Down (Lyrics)']

def init():
    spotify = spotify_connector()
    
    for song in playlist_songs:
        print("BEFORE {}  AFTER {}".format(song, StringUtils.clean_queriable(song)))
    
    songs_touples = CollectionUtils.element_to_tuple_by_separator(coll=playlist_songs, separator="-")
    print("SONGS {}".format(songs_touples))
    spotify_uris = []
    not_found_songs = []
    for tuple in songs_touples:
        coso = spotify.search_for_song(artist_name=tuple[0], song_name=tuple[1])

if __name__ == "__main__":
    init()
