from django.shortcuts import render
import sys
import os
import django
sys.path.append('/home/bjork/www/bjorktest.com/web')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()
from twitchstats.models import active_table_games, active_table_streams


def index(request):
    cat_streams = current_active_table = active_table_streams.objects.values().order_by('-id').first()
    cat_games = current_active_table = active_table_games.objects.values().order_by('-id').first()

    return render(request, 'templates/base.html', {'cat_streams': cat_streams, 'cat_games': cat_games})
