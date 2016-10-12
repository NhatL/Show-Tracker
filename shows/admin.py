from django.contrib import admin

from models import *


class GenreInline(admin.TabularInline):
    model = Genre.show.through
    extra = 0


class SeasonInline(admin.TabularInline):
    model = Season
    readonly_fields = ('number', 'movie_db_id', )
    exclude = ('description', 'server_img_path', 'local_img_path', )
    extra = 0


class EpisodeInline(admin.TabularInline):
    model = Episode
    readonly_fields = ('movie_db_id', )
    exclude = ('description', )
    extra = 0


class ShowAdmin(admin.ModelAdmin):
    inlines = [GenreInline, SeasonInline]
    list_display = ('name', 'ongoing', 'popularity', 'episode_count', )


class SeasonAdmin(admin.ModelAdmin):
    inlines = [EpisodeInline]
    list_display = ('show', 'number', )


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('number', 'season', 'title', 'air_date', )


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'movie_db_id', )


admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Show, ShowAdmin)
admin.site.register(Genre, GenreAdmin)
