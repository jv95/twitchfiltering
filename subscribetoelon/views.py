import os
import sys

import django
import yaml
from django.shortcuts import render

from web.settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()


def index(request):
    return render(request, 'subscribetoelon/templates/base.html')
