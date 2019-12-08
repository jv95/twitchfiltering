import os
import sys

import django
import yaml
from django.shortcuts import render

with open('settings.yaml', 'r') as yamlfile: cfg = yaml.load(yamlfile)
sys.path.append(cfg['environment']['sys_path_append'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()
from twitchstats.models import active_table_games, active_table_streams


def index(request):
    cat_streams = active_table_streams.objects.values().order_by('-id').first()
    cat_games = active_table_games.objects.values().order_by('-id').first()

    return render(request, 'templates/base.html', {'cat_streams': cat_streams, 'cat_games': cat_games})
