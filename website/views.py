from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

from shows.models import Show, Genre

import datetime


def index(request):
    print "index"
    return render(request, "website/index.html")


def popular(request):
    print "popular"
    return render(request, "website/index.html")


def show_details(request, id):
    print "show_details: " + str(id)
    try:
        show = Show.objects.get(movie_db_id=id)
    except ObjectDoesNotExist:
        args = {
            'error': 'Does not exist',
        }
    else:
        args = {
            'name': show.name,
            'popularity': show.popularity,
            'description': show.description,
            'ongoing': show.ongoing,
            'episode_count': show.episode_count,
            'seasons': [],
        }
        for season in show.season_set.all().order_by('number'):
            season_info = {
                'number': season.number,
            }
            episode_info = []
            for episode in season.episode_set.all():
                episode_detail = {
                    'title': episode.title,
                    'air_date': datetime.datetime.strftime(episode.air_date, "%b %d, %Y"),
                    'description': episode.description,
                    'number': "%02dx%02d" % (season.number, episode.number),
                }
                episode_info.append(episode_detail)
            season_info['episodes'] = episode_info
            args['seasons'].append(season_info)
    print args

    return render(request, "website/show_details.html", args)


def browse(request):
    args = {
        'genres': Genre.objects.values_list('name', flat=True),
        'genre': request.GET.get('genre', 'any'),
        'status': request.GET.get('status', 'any'),
        'name': request.GET.get('name', ''),
        'showAge': request.GET.get('showAge', 'any'),
    }
    if request.GET != {}:
        search_query = Q()

        if 'name' in request.GET and request.GET['name'] != '':
            args['search_string'] = request.GET['name']
            search_query = search_query & Q(name__contains=request.GET.get('name'))

        if 'genre' in request.GET and request.GET['genre'] != 'any':
            search_query = search_query & Q(genre=Genre.objects.get(name=request.GET['genre']))

        if 'status' in request.GET:
            if request.GET['status'] == 'running':
                search_query = search_query & Q(ongoing=True)
            if request.GET['status'] == 'ended':
                search_query = search_query & Q(ongoing=False)

        if 'showAge' in request.GET:
            if request.GET['showAge'] == 'morethan1':
                search_query = search_query & Q(first_air__lte=datetime.datetime.now() - datetime.timedelta(days=365))
            if request.GET['showAge'] == 'lessthan1':
                search_query = search_query & Q(first_air__gte=datetime.datetime.now() - datetime.timedelta(days=365))

        results = Show.objects.filter(search_query).values('movie_db_id', 'name', 'popularity', 'description', 'episode_count', 'ongoing')

        paginator = Paginator(results, settings.DOWNLOAD_PAGINATOR)
        page = request.GET.get('page')
        try:
            shows_result = paginator.page(page)
        except PageNotAnInteger:
            shows_result = paginator.page(1)
        except EmptyPage:
            shows_result = paginator.page(paginator.num_pages)

        args['paginator'] = shows_result
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
