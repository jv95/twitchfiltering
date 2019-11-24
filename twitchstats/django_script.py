#!/usr/bin/python3
# coding=utf8

from twitchstats.streams_manager import StreamsManager
from twitchstats.games_manager import GamesManager

get_all_streams = StreamsManager()
get_all_games = GamesManager()

get_all_streams.get_streams()
get_all_games.get_games()