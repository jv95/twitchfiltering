#!/usr/bin/python3
# coding=utf8


import logging

from modules import games_manager
from modules import streams_manager

logging.basicConfig(filename='django_script.log', format='%(asctime)s')
try:
    get_all_streams = streams_manager.StreamsManager()
    get_all_games = games_manager.GamesManager()
    get_all_streams.get_streams()
    get_all_games.get_games()
except Exception as e:
    logging.exception('Exception has occured!')
