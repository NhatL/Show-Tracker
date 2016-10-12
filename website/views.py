from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from shows.models import Show, Genre


def index(request):
    print "index"
    return render(request, "website/index.html")


def popular(request):
    print "popular"
    return render(request, "website/index.html")


def show_details(request, id):
    print "show_details: " + str(id)
    return render(request, "website/show_details.html")


def browse(request):
    args = {
        'genres': Genre.objects.values_list('name', flat=True),
        'genre': request.GET.get('genre', 'any'),
        'status': request.GET.get('status', 'any'),
        'name': request.GET.get('name', ''),
        'showAge': request.GET.get('showAge', 'any'),
    }
    print request.GET
    if request.GET != {}:
        search_query = Q()

        if 'name' in request.GET and request.GET['name'] != '':
            args['search_string'] = request.GET['name']
            search_query = search_query & Q(name__contains=request.GET.get('name'))

        if request.GET['genre'] != 'any':
            search_query = search_query & Q(genre=Genre.objects.get(name=request.GET['genre']))

        if request.GET['status'] == 'running':
            search_query = search_query & Q(ongoing=True)
        if request.GET['status'] == 'ended':
            search_query = search_query & Q(ongoing=False)

        results = Show.objects.filter(search_query).values_list('name', 'popularity', 'description', 'episode_count', 'ongoing')

        paginator = Paginator(results, settings.DOWNLOAD_PAGINATOR)
        page = request.GET.get('page')
        try:
            shows_result = paginator.page(page)
        except PageNotAnInteger:
            shows_result = paginator.page(1)
        except EmptyPage:
            shows_result = paginator.page(paginator.num_pages)

        args['paginator'] = shows_result
    print args
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
