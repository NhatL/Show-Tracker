from shows.models import Show, Genre
from shows.api import discover

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        print "PULL SHOW DETAILS"
        all_shows = {}
        for i in range(1, 1001):
            result = discover(page=i)
            print result
            for show in result:
                new_show = Show.objects.get_or_create(movie_db_id=show['id'])[0]
                new_show.name = show['name']
                print show['genre_ids']
                new_show.genre_set = [Genre.objects.get(movie_db_id=d) for d in show['genre_ids']]
                new_show.save()
