import os
import sys

import django
import yaml
from django.shortcuts import render
from web.settings import BASE_DIR

with open(BASE_DIR + '/twitchstats/settings.yaml', 'r') as yamlfile: cfg = yaml.load(yamlfile)
sys.path.append(cfg['environment']['sys_path_append'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()
from twitchstats.forms import GetStreamsForm
from twitchstats.models import active_table_streams, live_streams, live_streams2


def index(request):
    form = GetStreamsForm()
    if request.GET.get('game'):
        game = request.GET.get('game')
        maxv = request.GET.get('max_viewers')
        language = request.GET.get('language')
        form_updated = GetStreamsForm(initial={'game': game, 'max_viewers': maxv, 'language': language})

        active_table_str = active_table_streams.objects.values()
        if maxv and language:
            stream_list = live_streams2.objects.values().filter(game_id=game,
                                                                viewer_count__lte=maxv,
                                                                language=language) if 'live_streams2' in active_table_str else live_streams.objects.values().filter(
                game_id=game, viewer_count__lte=maxv, language=language)
        elif maxv:
            stream_list = live_streams2.objects.values().filter(game_id=game,
                                                                viewer_count__lte=maxv) if 'live_streams2' in active_table_str else live_streams.objects.values().filter(
                game_id=game, viewer_count__lte=maxv)
        else:
            stream_list = live_streams2.objects.values().filter(
                game_id=game) if 'live_streams2' in active_table_str else live_streams.objects.values().filter(
                game_id=game)
        for d in stream_list:
            if d['thumbnail_url']:
                value = str(d['thumbnail_url'])
                d['thumbnail_url'] = value.replace('{width}x{height}', '315x178')
        return render(request, 'templates/base.html', {'form': form_updated, 'response': stream_list})
    return render(request, 'templates/base.html', {'form': form})
