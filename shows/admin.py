from django.contrib import admin

from models import *



class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'ongoing', )


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('show', 'number', )


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('number', 'season', 'title', )


admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Show, ShowAdmin)
