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


def index(request):
    form = GetStreamsForm()
    if request.GET.get('game'):
        response = request.GET.get('game')
        maxf = request.GET.get('max_followers')
        maxv = request.GET.get('max_viewers')
        form_updated = GetStreamsForm(initial={'game': response, 'max_followers': maxf, 'max_viewers': maxv})
        return render(request, 'templates/base.html', {'form': form_updated, 'response': response, 'maxf': maxf, 'maxv': maxv})
    return render(request, 'templates/base.html', {'form': form})
