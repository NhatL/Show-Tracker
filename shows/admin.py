from django.contrib import admin

from models import *


class GenreInline(admin.TabularInline):
    model = Genre.show.through


class ShowAdmin(admin.ModelAdmin):
    inline = (GenreInline, )
    list_display = ('name', 'ongoing', )


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('show', 'number', )


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('number', 'season', 'title', )



class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'movie_db_id', )


admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Show, ShowAdmin)
admin.site.register(Genre, GenreAdmin)
