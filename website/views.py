from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

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
        return redirect(reverse('browse-view'))
    else:
        args = {
            'name': show.name,
            'popularity': show.popularity,
            'description': show.description,
            'ongoing': show.ongoing,
            'episode_count': show.episode_count,
            'vote_average': show.vote_average,
            'vote_count': show.vote_count,
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

        results = Show.objects.filter(search_query).values('movie_db_id', 'name', 'popularity', 'description', 'episode_count', 'ongoing', 'vote_average', 'vote_count')

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
    print request.user.show_set.all()
    return render(request, "website/my_shows.html")


def login_user(request):
    print "login"

    if request.user.is_authenticated():
        return redirect(reverse('main-view'))

    if request.POST:
        email = request.POST['email']
        password = request.POST['password']

        try:
            validate_email(email)
        except:
            return render(request, "website/login.html", {'error': "Bad email.", 'email': email, 'password': password})
        else:
            pass

        wanted_user = User.objects.filter(email=email)
        if len(wanted_user) > 1:
            return redirect(reverse('login-view'))
        if len(wanted_user) < 1:
            return render(request, "website/login.html", {'error': "Email doesn't exist.", 'email': email, 'password': password})

        wanted_user = wanted_user[0]
        user = authenticate(username=wanted_user.username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('main-view'))
        else:
            return render(request, "website/login.html", {'error': "Wrong password.", 'email': email, 'password': password})
    return render(request, "website/login.html")


def signup(request):
    print "signup"
    if request.user.is_authenticated():
        return redirect(reverse('main-view'))

    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            return render(request, "website/signup.html", {
                'error': "Passwords doesn't match.",
                'email': email,
                'password': password,
                'password_confirm': password_confirm
            })

        try:
            validate_email(email)
        except:
            return render(request, "website/signup.html", {
                'error': "Bad email.",
                'email': email,
                'password': password,
                'password_confirm': password_confirm
            })
        else:
            pass

        checked_users = User.objects.filter(email=email)
        if len(checked_users) > 0:
            return render(request, "website/signup.html", {
                'error': "Email already exists.",
                'email': email,
                'password': password,
                'password_confirm': password_confirm
            })

        user = User.objects.create_user(email, email, password)
        user.save()

        user = authenticate(username=email, password=password)
        if user.is_active:
            login(request, user)
            return redirect(reverse('main-view'))

    return render(request, "website/signup.html")


def profile(request):
    print "profile"
    return render(request, "website/index.html")


def reset(request):
    print "reset"
    return render(request, "website/reset.html")
