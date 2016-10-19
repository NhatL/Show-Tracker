from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.validators import validate_email

from shows.models import Show, Genre, Episode

import datetime


def index(request):
    args = {
        'site_title': 'Homepage',
    }
    return render(request, "website/index.html", args)


def others(request, etc):
    return redirect(reverse('main-view'))


def popular(request):
    genres = Genre.objects.order_by('name')

    args = {
        'site_title': 'Popular shows',
        'genres': [],
    }

    for genre in genres:
        args['genres'].append({
            'name': genre.name,
            'shows': [{
                'name': d.name,
                'popularity': d.popularity,
                'vote_average': d.vote_average,
                'vote_count': d.vote_count,
                'episode_count': d.episode_count,
                'ongoing': d.ongoing,
                'description': d.description,
                'id': d.movie_db_id,
            } for d in genre.show.extra(
                select={'total': '1.0 * vote_average * vote_count / popularity'},
                order_by=['-total'],
            )[:10]]
        })
    return render(request, "website/popular.html", args)


def show_details(request, id):
    try:
        show = Show.objects.get(movie_db_id=id)
    except ObjectDoesNotExist:
        return redirect(reverse('browse-view'))
    else:
        pass

    args = {
        'site_title': show.name,
        'name': show.name,
        'popularity': show.popularity,
        'description': show.description,
        'ongoing': show.ongoing,
        'episode_count': show.episode_count,
        'vote_average': show.vote_average,
        'vote_count': show.vote_count,
        'seasons': [],
        'id': id,
    }
    if request.user.is_authenticated():
        args['has_show'] = show in request.user.show_set.all()

    for season in show.season_set.order_by('number'):
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
                'watched': episode in request.user.userprofile.watched_episodes.all(),
                'id': episode.movie_db_id,
            }
            episode_info.append(episode_detail)
        season_info['episodes'] = episode_info
        args['seasons'].append(season_info)

    return render(request, "website/show_details.html", args)


def browse(request):
    args = {
        'site_title': "Browse",
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
    if not request.user.is_authenticated():
        return redirect(reverse('login-view'))

    args = {
        'site_title': "Unwatched shows",
        'show': [],
    }
    watched_episodes = request.user.userprofile.watched_episodes.all()
    episodes = []
    shows = []

    for show in request.user.show_set.all():
        for season in show.season_set.all():
            for episode in season.episode_set.all():
                episodes.append(episode)

    for episode in episodes:
        if episode not in watched_episodes:
            episode_info = {
                'number': episode.number,
                'title': episode.title,
                'air_date': episode.air_date,
                'description': episode.description,
                'episode_id': episode.movie_db_id,
                'unicode': episode.__unicode__(),
                'show_id': episode.season.show.movie_db_id,
            }
            shows.append(episode_info)

    args['episodes'] = shows
    print args
    return render(request, "website/unwatched.html", args)


def my_shows(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login-view'))

    args = {
        'site_title': "My shows",
    }
    all_watched = request.user.userprofile.watched_episodes.all()[:]

    now = datetime.datetime.now().date()
    all_shows = []
    for show in request.user.show_set.all():
        episodes_before = []
        episodes_after = []
        not_watched = 0
        for season in show.season_set.all():
            for episode in season.episode_set.all():
                if episode.air_date < now:
                    episodes_before.append(episode)
                else:
                    episodes_after.append(episode)

                if episode in all_watched:
                    not_watched += 1
        episodes_before.sort(key=lambda x: x.air_date, reverse=True)
        episodes_after.sort(key=lambda x: x.air_date, reverse=False)

        if len(episodes_before) < 1:
            last_episode = {
                'name': '-',
            }
        else:
            last_episode = {
                'name': episodes_before[0].__unicode__,
                'date': datetime.datetime.strftime(episodes_before[0].air_date, "%b %d, %Y"),
            }

        if len(episodes_after) < 1:
            next_episode = {
                'name': '-',
            }
        else:
            next_episode = {
                'name': episodes_after[0].__unicode__,
                'date': datetime.datetime.strftime(episodes_after[0].air_date, "%b %d, %Y"),
            }

        all_shows.append({
            'name': show.name,
            'id': show.movie_db_id,
            'last': last_episode,
            'next': next_episode,
            'not_watched': not_watched,
        })

    args['shows'] = all_shows
    return render(request, "website/my_shows.html", args)


def my_shows_remove(request, id):
    if not request.user.is_authenticated():
        return redirect(reverse('login-view'))

    try:
        show = Show.objects.get(movie_db_id=id)
    except:
        return redirect(reverse('my-shows-view'))
    else:
        pass

    if show not in request.user.show_set.all():
        return redirect(reverse('my-shows-view'))

    for episode in request.user.userprofile.watched_episodes.all():
        if episode.season.show == show:
            request.user.userprofile.watched_episodes.remove(episode)

    request.user.show_set.remove(show)

    return redirect(reverse('my-shows-view'))


def my_shows_add(request, id):
    if not request.user.is_authenticated():
        return redirect(reverse('login-view'))

    try:
        show = Show.objects.get(movie_db_id=id)
    except:
        return redirect(reverse('my-shows-view'))
    else:
        pass

    if show in request.user.show_set.all():
        return redirect(reverse('my-shows-view'))
    request.user.show_set.add(show)

    return redirect(reverse('my-shows-view'))


def my_show_episode(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login-view'))

    if request.method == "POST":
        if 'id' in request.POST and 'new_value' in request.POST:
            episode_id = request.POST['id']
            new_value = request.POST['new_value'].upper()

            try:
                episode_id = int(episode_id)
                if new_value == "TRUE":
                    new_value = True
                elif new_value == "FALSE":
                    new_value = False
                else:
                    raise Exception
                episode = Episode.objects.get(movie_db_id=episode_id)

                if request.user not in episode.season.show.users.all():
                    raise Exception

                user_watched = request.user.userprofile.watched_episodes.all()

                if episode in user_watched and not new_value:
                    # Episode is watched and now it is marked as Unwatched -> do it
                    request.user.userprofile.watched_episodes.remove(episode)
                elif episode not in user_watched and new_value:
                    # Episode is unwatched and now it is marked as Watched -> do it
                    request.user.userprofile.watched_episodes.add(episode)
                else:
                    raise Exception
            except:
                return redirect(reverse('main-view'))
            else:
                pass
        else:
            return redirect(reverse('main-view'))
    else:
        return redirect(reverse('main-view'))


def my_show_mark_all(request, id):
    if not request.user.is_authenticated():
        return redirect(reverse('main-view'))

    try:
        show = Show.objects.get(movie_db_id=id)

        if show not in request.user.show_set.all():
            raise Exception

        for season in show.season_set.all():
            for episode in season.episode_set.all():
                if episode not in request.user.userprofile.watched_episodes.all():
                    request.user.userprofile.watched_episodes.add(episode)
    except:
        return redirect(reverse('main-view'))
    else:
        return redirect(reverse('main-view'))


def my_show_mark_season(request, id, season_number):
    try:
        if not request.user.is_authenticated():
            raise Exception

        show = Show.objects.get(movie_db_id=id)

        if show not in request.user.show_set.all():
            raise Exception

        for season in show.season_set.all():
            if str(season.number) == str(season_number):
                for episode in season.episode_set.all():
                    if episode not in request.user.userprofile.watched_episodes.all():
                        request.user.userprofile.watched_episodes.add(episode)
                break
    except:
        pass

    return redirect(reverse('main-view'))


def my_show_mark_season_unwatched(request, id, season_number):
    try:
        if not request.user.is_authenticated():
            raise Exception

        show = Show.objects.get(movie_db_id=id)

        if show not in request.user.show_set.all():
            raise Exception

        for season in show.season_set.all():
            if str(season.number) == str(season_number):
                for episode in season.episode_set.all():
                    if episode in request.user.userprofile.watched_episodes.all():
                        request.user.userprofile.watched_episodes.remove(episode)
                break
    except:
        pass

    return redirect(reverse('main-view'))



def login_user(request):
    if request.user.is_authenticated():
        return redirect(reverse('main-view'))

    args = {
        'site_title': "Login",
    }

    if request.method == "POST":
        try:
            email = request.POST['email']
            password = request.POST['password']
        except:
            args['error'] = "No email & password specified."
            return render(request, "website/login.html", args)
        else:
            pass

        args['email'] = email
        args['password'] = password
        try:
            validate_email(email)
        except:
            args['error'] = "Bad email."
            return render(request, "website/login.html", args)
        else:
            pass

        wanted_user = User.objects.filter(email=email)
        if len(wanted_user) > 1:
            return redirect(reverse('login-view'))
        if len(wanted_user) < 1:
            args['error'] = "Email doesn't exist."
            return render(request, "website/login.html", args)

        wanted_user = wanted_user[0]
        user = authenticate(username=wanted_user.username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('main-view'))
        else:
            args['error'] = 'Wrong password.'
            return render(request, "website/login.html", args)
    return render(request, "website/login.html", args)


def signup(request):
    if request.user.is_authenticated():
        return redirect(reverse('main-view'))

    args = {
        'site_title': "Signup",
    }

    if request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        args['first_name'] = first_name
        args['last_name'] = last_name
        args['email'] = email
        args['password'] = password
        args['password_confirm'] = password_confirm

        if password != password_confirm:
            args['error'] = "Passwords doesn't match."
            return render(request, "website/signup.html", args)

        try:
            validate_email(email)
        except:
            args['error'] = "Bad email."
            return render(request, "website/signup.html", args)
        else:
            pass

        checked_users = User.objects.filter(email=email)
        if len(checked_users) > 0:
            args['error'] = "Email already exists."
            return render(request, "website/signup.html", args)

        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        user = authenticate(username=email, password=password)
        if user.is_active:
            login(request, user)
            return redirect(reverse('main-view'))

    return render(request, "website/signup.html", args)


def profile(request):
    if not request.user.is_authenticated():
        return redirect(reverse('login-view'))

    user = request.user

    args = {
        'site_title': "Profile of " + user.first_name,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }

    if request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        new_password = request.POST['new_password']
        password_confirm = request.POST['password_confirm']

        if new_password != '' and new_password != password_confirm:
            args['error'] = "Passwords doesn't match."
            args['password'] = password
            args['new_password'] = new_password
            args['password_confirm'] = password_confirm
            return render(request, "website/profile.html", args)

        try:
            validate_email(email)
        except:
            args['error'] = "Bad email."
            args['password'] = password
            args['new_password'] = new_password
            args['password_confirm'] = password_confirm
            return render(request, "website/profile.html", args)
        else:
            pass

        checked_users = User.objects.filter(email=email)
        if len(checked_users) > 0 and request.user.id != checked_users[0].id:
            args['error'] = "Email already exists."
            args['password'] = password
            return render(request, "website/profile.html", args)

        if not user.check_password(password):
            args['error'] = "Wrong password."
            args['first_name'] = first_name
            args['last_name'] = last_name
            args['email'] = email
            args['password'] = password
            args['new_password'] = new_password
            args['password_confirm'] = password_confirm
            return render(request, "website/profile.html", args)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = email if not user.is_superuser else user.username
        user.set_password(new_password)
        user.save()
        return redirect(reverse('login-view'))

    return render(request, "website/profile.html", args)


def reset(request):
    if request.user.is_authenticated():
        return redirect(reverse('main-view'))

    args = {
        'site_title': 'Reset Password',
    }

    if request.POST:
        email = request.POST['email']

        users = User.objects.filter(email=email)

        if len(users) == 0:
            args['error'] = "Email doesn't exist."
            args['email'] = email
            return render(request, "website/reset.html", args)

        args['success'] = 'Email has been reseted. Check your email for further instructions.'

    return render(request, "website/reset.html", args)
