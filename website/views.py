from django.shortcuts import render

from shows.api import *


def index(request):
    return render(request, "website/index.html")
