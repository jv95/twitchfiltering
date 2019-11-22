#!/usr/bin/python3
# coding=utf8

# code needs improvements!, get system specific values from sys variables, create new db everytime,
# then delete the old one and replace it with the new one

import os
import sys
import time
from datetime import datetime

import django
import requests

event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
sys.path.append("/home/bjork/www/bjorktest.com/web")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()
from twitchstats.models import live_streams, live_streams_performance, game_identity, game_identity_performance

# stream list
HEADER = {"Client-ID": "8p8mneffjoj1ilw5jxfkblh5hzsh5e"}
ENDPOINT = " https://api.twitch.tv/helix/streams?first=100"
endpoint2 = " https://api.twitch.tv/helix/streams?first=100&after="
request_count = 1

games = requests.get(ENDPOINT, headers=HEADER).json()
paginator = games['pagination']['cursor']
datatoprocess = games['data']
number_of_streams = 0
live_streams.objects.all().delete()
data_uploading_start_time = time.time()
streams_for_bulk = []
while paginator != '':
    games2 = requests.get(endpoint2 + paginator, headers=HEADER).json()
    request_count += 1
    if 'data' in games2:
        datatoprocess = games2['data']
        paginator = games2['pagination']['cursor'] if 'cursor' in games2['pagination'] else ''
        for i in range(0, len(datatoprocess)):
            live_stream = live_streams(stream_id=datatoprocess[i]['id'],
                                       user_id=datatoprocess[i]['user_id'],
                                       user_name=datatoprocess[i]['user_name'],
                                       game_id=datatoprocess[i]['game_id'],
                                       type=datatoprocess[i]['type'],
                                       title=datatoprocess[i]['title'],
                                       viewer_count=datatoprocess[i]['viewer_count'],
                                       started_at=datatoprocess[i]['started_at'],
                                       language=datatoprocess[i]['language'],
                                       thumbnail_url=datatoprocess[i]['thumbnail_url'],
                                       tag_ids=datatoprocess[i]['tag_ids'])
            streams_for_bulk.append(live_stream)
            live_streams.objects.bulk_create(streams_for_bulk, 10000)
            streams_for_bulk = []
        number_of_streams += len(datatoprocess)
        datatoprocess.clear()
    else:
        break
    # make a logger here
live_streams.objects.bulk_create(streams_for_bulk)
data_uploading_time = time.time() - data_uploading_start_time

performance = live_streams_performance(date=event_time,
                                       number_of_streams=number_of_streams,
                                       data_requesting_time=0,
                                       data_uploading_time=0,
                                       final_time=data_uploading_time,
                                       request_count=request_count)
performance.save()

# game list
event_time_games = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
requesting_start_time_games = time.time()

ENDPOINT_games = " https://api.twitch.tv/helix/games/top?first=100"
endpoint2_games = " https://api.twitch.tv/helix/games/top?first=100&after="
request_count_games = 1
games_games = requests.get(ENDPOINT_games, headers=HEADER).json()
paginator_games = games_games['pagination']['cursor']
gamelist = games_games['data']
games_for_bulk = []
game_identity.objects.all().delete()
data_uploading_start_time_games = time.time()
number_of_games = 0

while paginator_games != '':
    games2_games = requests.get(endpoint2_games + paginator_games, headers=HEADER).json()
    request_count_games += 1
    if 'data' in games2_games:
        gamelist = games2_games['data']
        paginator_games = games2_games['pagination']['cursor'] if 'cursor' in games2_games['pagination'] else ''
        for i in range(0, len(gamelist)):
            games_identity = game_identity(game_id=gamelist[i]['id'],
                                           game_name=gamelist[i]['name'],
                                           box_art_url=gamelist[i]['box_art_url'])
            games_for_bulk.append(games_identity)
            game_identity.objects.bulk_create(games_for_bulk, 10)
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