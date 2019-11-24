#!/usr/bin/python3
# coding=utf8

from streams_manager import StreamsManager
from games_manager import GamesManager

get_all_streams = StreamsManager()
get_all_games = GamesManager()

get_all_streams.get_streams()
get_all_games.get_games()
