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
from twitchstats.models import game_identity, game_identity_performance, game_identity2, active_table_games


class GamesManager:
    def __init__(self):
        self.HEADER = {"Client-ID": cfg['twitch']['client_id']}

    def get_games(self):
        event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ENDPOINT = " https://api.twitch.tv/helix/games/top?first=100"
        endpoint2 = " https://api.twitch.tv/helix/games/top?first=100&after="
        request_count = 1
        number_of_games = 0
        games_for_bulk = []
        current_active_table = active_table_games.objects.values().order_by('-id').first()
        current_inactive_table = game_identity2 if current_active_table['active_table'] == '<class \'twitchstats.models.game_identity\'>' else game_identity

        data_uploading_start_time = time.time()
        games = requests.get(ENDPOINT, headers=self.HEADER).json()
        paginator = games['pagination']['cursor']
        game_list = games['data']
        number_of_games += len(game_list)
        current_inactive_table.objects.all().delete()

        while paginator != '':
            games2 = requests.get(endpoint2 + paginator, headers=self.HEADER).json()
            request_count += 1
            if request_count >= cfg['twitch']['max_games_request_count']: break
            if 'data' in games2:
                game_list += games2['data']
                paginator = games2['pagination']['cursor'] if 'cursor' in games2['pagination'] else ''
                for i in range(0, len(game_list)):
                    games_identity = current_inactive_table(game_id=game_list[i]['id'],
                                                   game_name=game_list[i]['name'],
                                                   box_art_url=game_list[i]['box_art_url'])
                    games_for_bulk.append(games_identity)
                current_inactive_table.objects.bulk_create(games_for_bulk, ignore_conflicts=True)
                number_of_games += len(game_list)
                games_for_bulk.clear()
                games2.clear()
                game_list.clear()
            else:
                break

        active_table_games.objects.all().delete()
        new_active_table = active_table_games(active_table=str(current_inactive_table))
        new_active_table.save()
        performance_games = game_identity_performance(date=event_time,
                                                      number_of_games=number_of_games,
                                                      final_time=time.time() - data_uploading_start_time,
                                                      request_count=request_count)
        performance_games.save()


if __name__ == '__main__':
    get_all_games = GamesManager()
    get_all_games.get_games()
