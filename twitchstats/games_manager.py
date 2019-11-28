#!/usr/bin/python3
# coding=utf8

# code needs improvements!, get system specific values from yaml, create new db everytime,
# then delete the old one and replace it with the new one

import os
import sys
import time
from datetime import datetime
import yaml

import django
import requests

with open('settings.yaml', 'r') as yamlfile:
    cfg = yaml.load(yamlfile)

event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
sys.path.append(cfg['environment']['sys_path_append'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()
from twitchstats.models import game_identity, game_identity_performance


class GamesManager:
    def __init__(self):
        self.HEADER = {"Client-ID": cfg['twitch']['client_id']}

    def get_games(self):

        event_time_games = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        requesting_start_time_games = time.time()

        ENDPOINT_games = " https://api.twitch.tv/helix/games/top?first=100"
        endpoint2_games = " https://api.twitch.tv/helix/games/top?first=100&after="
        request_count_games = 1
        games_games = requests.get(ENDPOINT_games, headers=self.HEADER).json()
        paginator_games = games_games['pagination']['cursor']
        gamelist = games_games['data']
        games_for_bulk = []
        game_identity.objects.all().delete()
        data_uploading_start_time_games = time.time()
        number_of_games = 0
        number_of_games += len(gamelist)

        while paginator_games != '':
            games2_games = requests.get(endpoint2_games + paginator_games, headers=self.HEADER).json()
            request_count_games += 1
            if 'data' in games2_games:
                gamelist += games2_games['data']
                paginator_games = games2_games['pagination']['cursor'] if 'cursor' in games2_games['pagination'] else ''
                games2_games.clear()
                for i in range(0, len(gamelist)):
                    games_identity = game_identity(game_id=gamelist[i]['id'],
                                               game_name=gamelist[i]['name'],
                                               box_art_url=gamelist[i]['box_art_url'])
                    games_for_bulk.append(games_identity)
                game_identity.objects.bulk_create(games_for_bulk)
                games_for_bulk = []
                number_of_games += len(gamelist)
                gamelist.clear()
            else:
                break
        game_identity.objects.bulk_create(games_for_bulk)
        data_uploading_time_games = time.time() - data_uploading_start_time_games
        performance_games = game_identity_performance(date=event_time_games,
                                                  number_of_games=number_of_games,
                                                  data_requesting_time=0,
                                                  data_uploading_time=0,
                                                  final_time=data_uploading_time_games,
                                                  request_count=request_count_games)
        performance_games.save()

if __name__ == '__main__':
    get_all_games = GamesManager()
    get_all_games.get_games()