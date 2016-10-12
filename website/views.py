from django.shortcuts import render

from shows.models import Show

def index(request):
    print "index"
    return render(request, "website/index.html")


def popular(request):
    print "popular"
    return render(request, "website/index.html")


def browse(request):
    print "Browse"
    args = {}
    if 'name' in request.GET:
        print request.GET
        args['search_string'] = request.GET['name']
    return render(request, "website/browse.html", args)


def unwatched(request):
    print "Unwatched"
    return render(request, "website/index.html")


def my_shows(request):
    print "mine"
    return render(request, "website/index.html")


def login(request):
    print "login"
    return render(request, "website/index.html")


def signup(request):
    print "signup"
    return render(request, "website/index.html")


def profile(request):
    print "profile"
    return render(request, "website/index.html")


def logout(request):
    print "logout"
    return render(request, "website/index.html")
