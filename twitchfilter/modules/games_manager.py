#!/usr/bin/python3
# coding=utf8

import os
import sys
import time
from datetime import datetime

import django
import requests
import yaml

with open('settings.yaml', 'r') as yamlfile: cfg = yaml.load(yamlfile)
sys.path.append(cfg['environment']['sys_path_append'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()
from twitchfilter.models import game_identity, game_identity_performance
from django.db import transaction


class GamesManager:
    def __init__(self):
        self.HEADER = {"Client-ID": cfg['twitch']['client_id']}

    @transaction.atomic
    def get_games(self):
        event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ENDPOINT = " https://api.twitch.tv/helix/games/top?first=100"
        endpoint2 = " https://api.twitch.tv/helix/games/top?first=100&after="
        request_count = 1
        number_of_games = 0
        games_for_bulk = []
        game_identity.objects.all().delete()
        data_uploading_start_time = time.time()
        games = requests.get(ENDPOINT, headers=self.HEADER).json()
        paginator = games['pagination']['cursor']
        game_list = games['data']
        number_of_games += len(game_list)

        while paginator != '':
            games2 = requests.get(endpoint2 + paginator, headers=self.HEADER).json()
            request_count += 1
            if request_count >= cfg['twitch']['max_games_request_count']: break
            if 'data' in games2:
                game_list += games2['data']
                paginator = games2['pagination']['cursor'] if 'cursor' in games2['pagination'] else ''
                for i in range(0, len(game_list)):
                    games_identity = game_identity(game_id=game_list[i]['id'],
                                                   game_name=game_list[i]['name'],
                                                   box_art_url=game_list[i]['box_art_url'])
                    games_for_bulk.append(games_identity)
                game_identity.objects.bulk_create(games_for_bulk, ignore_conflicts=True)
                number_of_games += len(game_list)
                games_for_bulk.clear()
                games2.clear()
                game_list.clear()
            else:
                break

        performance_games = game_identity_performance(date=event_time,
                                                      number_of_games=number_of_games,
                                                      final_time=time.time() - data_uploading_start_time,
                                                      request_count=request_count)
        performance_games.save()


if __name__ == '__main__':
    get_all_games = GamesManager()
    get_all_games.get_games()
