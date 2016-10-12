# -*- coding: utf-8 -*-
import datetime

from shows.models import Show, Genre, Season, Episode
from shows.api import discover, get_seasons, get_season_episodes

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        print "PULLING SHOW DETAILS"
        for i in range(1, 1001):
            print "----------- Current index: " + str(i)
            result = discover(page=i)
            for show in result:
                episode_count = 0
                if isinstance(show['name'], unicode):
                    print show['name'].encode('windows-1252', 'ignore')
                else:
                    print show['name']
                new_show = Show.objects.get_or_create(movie_db_id=show['id'])[0]
                new_show.name = show['name']
                new_show.description = show.get('overview', '')
                new_show.popularity = show.get('popularity', 1)
                new_show.genre_set = []
                for genre_id in show['genre_ids']:
                    try:
                        new_show.genre_set.add(Genre.objects.get(movie_db_id=genre_id))
                    except:
                        pass
                new_show.save()
                seasons = get_seasons(show['id'])
                for season in seasons:
                    if season.get('season_number', 1) is None:
                        season['season_number'] = 1
                        print "S None"
                    else:
                        print "S%02d" % season.get('season_number', 1)
                    new_season = Season.objects.get_or_create(movie_db_id=season['id'], number=season.get('season_number', 1), show=new_show)[0]
                    new_season.save()

                    episodes = get_season_episodes(tv_id=show['id'], season_number=season.get('season_number', 1))
                    for episode in episodes:
                        new_episode = Episode.objects.get_or_create(movie_db_id=episode['id'], number=episode.get('episode_number', 1), season=new_season)[0]
                        new_episode.description = episode['overview']
                        new_episode.title = episode['name']
                        if episode['air_date'] is None:
                            episode['air_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                        new_episode.air_date = datetime.datetime.strptime(episode.get('air_date', datetime.datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
                        new_episode.save()
                        episode_count += 1
                new_show.episode_count = episode_count
                new_show.save()