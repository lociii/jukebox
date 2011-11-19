# -*- coding: UTF-8 -*-

from models import Artist, Genre, Album, Song, Queue
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


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Queue, QueueAdmin)
