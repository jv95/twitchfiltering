import os
import sys

import django
import yaml
from django.shortcuts import render

from web.settings import BASE_DIR

with open(BASE_DIR + '/twitchfilter/settings.yaml', 'r') as yamlfile: cfg = yaml.load(yamlfile)
sys.path.append(cfg['environment']['sys_path_append'])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
from twitchfilter.forms import GetStreamsForm
from twitchfilter.models import live_streams


def index(request):
    form = GetStreamsForm()
    if request.GET:
        game = request.GET.get('game')
        maxv = request.GET.get('max_viewers')
        language = request.GET.get('language')
        form_updated = GetStreamsForm(initial={'game': game, 'max_viewers': maxv, 'language': language})
        if maxv and language and game:
            stream_list = live_streams.objects.values().filter(game_id=game, viewer_count__lte=maxv, language=language)
        elif game and language:
            stream_list = live_streams.objects.values().filter(game_id=game, language=language)
        elif maxv:
            stream_list = live_streams.objects.values().filter(viewer_count__lte=maxv)
        elif maxv and game:
            stream_list = live_streams.objects.values().filter(game_id=game, viewer_count__lte=maxv)
        elif game:
            stream_list = live_streams.objects.values().filter(game_id=game)
        elif language:
            stream_list = live_streams.objects.values().filter(language=language)
        elif language and maxv:
            stream_list = live_streams.objects.values().filter(language=language, viewer_count__lte=maxv)
        else:
            stream_list = live_streams.objects.values().filter()
        for d in stream_list:
            if d['thumbnail_url']:
                value = str(d['thumbnail_url'])
                d['thumbnail_url'] = value.replace('{width}x{height}', '315x178')
        return render(request, 'twitchfilter/templates/base.html', {'form': form_updated, 'response': stream_list})
    return render(request, 'twitchfilter/templates/base.html', {'form': form})
