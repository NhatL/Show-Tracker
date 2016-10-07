from shows.models import Genre
from shows.api import genres

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        result = genres()
        for genre_details in result:
            genre = Genre.objects.get_or_create(movie_db_id=genre_details['id'])[0]
            genre.name = genre_details['name']
            genre.save()
