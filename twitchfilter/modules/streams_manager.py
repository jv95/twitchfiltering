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
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
from twitchfilter.models import live_streams, live_streams_performance
from django.db import transaction


class StreamsManager:

    def __init__(self):
        self.HEADER = {'Client-ID': cfg['twitch']['client_id']}

    @transaction.atomic
    def get_streams(self):
        event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ENDPOINT = ' https://api.twitch.tv/helix/streams?first=100'
        endpoint2 = ' https://api.twitch.tv/helix/streams?first=100&after='
        request_count = 1
        number_of_streams = 0
        streams_for_bulk = []
        live_streams.objects.all().delete()
        data_uploading_start_time = time.time()
        streams = requests.get(ENDPOINT, headers=self.HEADER).json()
        paginator = streams['pagination']['cursor']
        stream_list = streams['data']
        number_of_streams += len(stream_list)

        while paginator != '':
            streams2 = requests.get(endpoint2 + paginator, headers=self.HEADER).json()
            request_count += 1
            if request_count >= cfg['twitch']['max_streams_request_count']: break
            if 'data' in streams2:
                stream_list += streams2['data']
                paginator = streams2['pagination']['cursor'] if 'cursor' in streams2['pagination'] else ''
                for i in range(0, len(stream_list)):
                    live_stream = live_streams(stream_id=stream_list[i]['id'],
                                               user_id=stream_list[i]['user_id'],
                                               user_name=stream_list[i]['user_name'],
                                               game_id=stream_list[i]['game_id'],
                                               type=stream_list[i]['type'],
                                               title=stream_list[i]['title'],
                                               viewer_count=stream_list[i]['viewer_count'],
                                               started_at=stream_list[i]['started_at'],
                                               language=stream_list[i]['language'],
                                               thumbnail_url=stream_list[i]['thumbnail_url'],
                                               tag_ids=stream_list[i]['tag_ids'])
                    streams_for_bulk.append(live_stream)
                live_streams.objects.bulk_create(streams_for_bulk, ignore_conflicts=True)
                number_of_streams += len(stream_list)
                streams_for_bulk.clear()
                streams2.clear()
                stream_list.clear()
            else:
                break

        performance = live_streams_performance(date=event_time,
                                               number_of_streams=number_of_streams,
                                               final_time=time.time() - data_uploading_start_time,
                                               request_count=request_count)
        performance.save()


if __name__ == '__main__':
    get_all_streams = StreamsManager()
    get_all_streams.get_streams()
