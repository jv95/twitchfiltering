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
    if form.is_valid():
        form.clean()

    return render(request, 'templates/base.html', {'form': form})
