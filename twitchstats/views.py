from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Something big is coming... stay tuned :)')
