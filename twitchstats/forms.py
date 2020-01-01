import os
import sys

import django
import yaml
from django import forms

from web.settings import BASE_DIR

with open(BASE_DIR + '/twitchstats/settings.yaml', 'r') as yamlfile: cfg = yaml.load(yamlfile)
sys.path.append(cfg['environment']['sys_path_append'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()
from twitchstats.models import game_identity, live_streams

game_list = game_identity.objects.values().order_by('game_name')
game_list_filtered = [d['game_name'] for d in game_list]
id_list_filtered = [d['game_id'] for d in game_list]
game_choices = zip(id_list_filtered, game_list_filtered)

streams_list = live_streams.objects.values(
    'language').order_by('language').distinct()
language_list = [d['language'] for d in streams_list]
language_to_choice = zip(language_list, language_list)


class GetStreamsForm(forms.Form):
    game = forms.ChoiceField(choices=game_choices, required=True,
                             widget=forms.Select(attrs={'class': 'form-control'}))
    max_viewers = forms.IntegerField(min_value=0, required=False,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    language = forms.ChoiceField(choices=language_to_choice, required=False,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
