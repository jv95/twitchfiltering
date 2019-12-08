from django.shortcuts import render

from twitchstats.models import active_table_games, active_table_streams

def index(request):
    cat_streams = active_table_streams.objects.values()
    cat_games = active_table_games.objects.values()
    return render(request, 'templates/base.html',
                  {'cat_streams': cat_streams[1]['active_table'], 'cat_games': cat_games[1]['active_table']})
