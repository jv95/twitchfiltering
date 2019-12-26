from django import forms
import os
import sys

import django
import yaml
from web.settings import BASE_DIR

with open(BASE_DIR + '/twitchstats/settings.yaml', 'r') as yamlfile: cfg = yaml.load(yamlfile)
sys.path.append(cfg['environment']['sys_path_append'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()
from twitchstats.models import game_identity, active_table_games, game_identity2

active_table_streams = active_table_games.objects.values()
game_list = game_identity2.objects.values() if 'game_identity2' in active_table_streams else game_identity.objects.values()
game_list_filtered = [d['game_name'] for d in game_list]
id_list_filtered = [d['game_id'] for d in game_list]
game_choices = zip(id_list_filtered, game_list_filtered)


class GetStreamsForm(forms.Form):
    game = forms.ChoiceField(choices=game_choices, required=True,
                             widget=forms.Select(attrs={'class': 'form-control'}))
    max_viewers = forms.IntegerField(min_value=0, required=False,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
