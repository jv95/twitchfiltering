#!/usr/bin/python3
# coding=utf8

# create new db everytime - delete the old one and replace it with the new one?

from games_manager import GamesManager
from streams_manager import StreamsManager

get_all_streams = StreamsManager()
get_all_games = GamesManager()

get_all_streams.get_streams()
get_all_games.get_games()
