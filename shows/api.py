# themoviedb API endpoints

# -*- coding:utf-8 -*-

from django.conf import settings

import requests
import os
import time
import json


api_key = settings.MOVIE_DB_API_KEY
root_api_url = settings.MOVIE_DB_ROOT_API_URL
api_limit_per_second = settings.MOVIE_DB_API_LIMIT_PER_SECOND


TV_URLS = {
    'details': 'tv/%(tv_id)s',
    'acc_state': 'tv/%(tv_id)s/account_states',
    'alt_title': 'tv/%(tv_id)s/alternative_titles',
    'changes': 'tv/%(tv_id)s/changes',
    'content_ratings': 'tv/%(tv_id)s/content_ratings',
    'credits': 'tv/%(tv_id)s/credits',
    'external_ids': 'tv/%(tv_id)s/external_ids',
    'images': 'tv/%(tv_id)s/images',
    'recommendations': 'tv/%(tv_id)s/recommendations',
    'similar': 'tv/%(tv_id)s/similar',
    'translations': 'tv/%(tv_id)s/translations',
    'latest': 'tv/latest',
    'airing_today': 'tv/airing_today',
    'on_the_air': 'tv/on_the_air',
    'popular': 'tv/popular',
    'top_rated': 'tv/top_rated',
}


TV_SEASON_URLS = {
    'details': 'tv/%(tv_id)s/season/%(season_number)s',
    'changes': 'tv/season/{season_id}/changes',
    'account_states': 'tv/%(tv_id)s/season/%(season_id)s/account_states',
    'credits': 'tv/%(tv_id)s/season/%(season_id)s/credits',
    'external_ids': 'tv/%(tv_id)s/season/%(season_id)s/external_ids',
    'images': 'tv/%(tv_id)s/season/%(season_id)s/images',
    'videos': 'tv/%(tv_id)s/season/%(season_id)s/videos',
}


DISCOVER_URLS = {
    'movie': 'discover/movie',
    'tv': 'discover/tv'
}

GENRE_URLS = {
    'movie': 'genre/movie/list',
    'tv': 'genre/tv/list'
}


def discover(type='tv', **kwargs):
    args = {
        'api_key': api_key,
    }
    for key, val in kwargs.iteritems():
        if isinstance(val, dict):
            for key2, val2 in val.iteritems():
                proper_key = key + "." + key2
                proper_val = val2
                args[proper_key] = proper_val
        else:
            args[key] = val
    request_url = os.path.join(root_api_url, DISCOVER_URLS[type]).replace('\\', '/')
    request_return = json.loads(requests.get(request_url, args).text)
    time.sleep(0.3)
    return request_return['results'] if 'results' in request_return else ''


def genres(type='tv', language='en-US'):
    # Return list of all genres
    args = {
        'api_key': api_key,
        'language': language,
    }
    request_url = os.path.join(root_api_url, GENRE_URLS[type]).replace('\\', '/')
    request_get = requests.get(request_url, args)
    request_return = json.loads(request_get.text)
    time.sleep(0.3)
    return request_return['genres'] if 'genres' in request_return else []


def get_seasons(id=1399):
    # Return seasons list by TV series ID
    args = {
        'api_key': api_key,
    }
    request_url = os.path.join(root_api_url, TV_URLS['details'] % ({'tv_id': id})).replace('\\', '/')
    request_get = requests.get(request_url, args)
    request_return = json.loads(request_get.text)
    time.sleep(0.3)
    return request_return['seasons'] if 'seasons' in request_return else []


def get_season_episodes(tv_id, season_number):
    # Return season detail by TV Show ID and Season number
    args = {
        'api_key': api_key,
    }
    request_url = os.path.join(root_api_url, TV_SEASON_URLS['details'] % ({'tv_id': tv_id, 'season_number': season_number})).replace('\\', '/')
    request_get = requests.get(request_url, args)
    request_return = json.loads(request_get.text)
    time.sleep(0.3)
    return request_return['episodes'] if 'episodes' in request_return else []
