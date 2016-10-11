from django.shortcuts import render

from shows.api import *


def index(request):
    return render(request, "website/index.html")


def popular(request):
    return render(request, "website/index.html")


def browse(request):
    return render(request, "website/index.html")


def unwatched(request):
    return render(request, "website/index.html")


def my_shows(request):
    return render(request, "website/index.html")


def login(request):
    return render(request, "website/index.html")


def signup(request):
    return render(request, "website/index.html")


def profile(request):
    return render(request, "website/index.html")


def logout(request):
    return render(request, "website/index.html")
