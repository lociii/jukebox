# -*- coding: UTF-8 -*-

from models import Artist, Genre, Album, Song, Queue, History, Favourite
from django.contrib import admin


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('Name', )
    search_fields = ['Name']


class GenreAdmin(admin.ModelAdmin):
    list_display = ('Name', )


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Artist', )
    search_fields = ['Title']


class SongAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Artist', 'Year', 'Genre', )
    search_fields = ['Title']


class QueueAdmin(admin.ModelAdmin):
    list_display = ('Song', 'Created', )


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('Song', 'Created', )


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('Song', 'User', 'Created', )
    search_fields = ['User__username']


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Queue, QueueAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Favourite, FavouriteAdmin)
