# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import patterns, url
import views

urlpatterns = patterns("",
    url(
        r"^api/v1/songs$",
        views.songs.as_view(),
        name="jukebox_api_songs"
    ),
    url(
        r"^api/v1/artists$",
        views.artists.as_view(),
        name="jukebox_api_artists"
    ),
    url(
        r"^api/v1/albums$",
        views.albums.as_view(),
        name="jukebox_api_albums"
    ),
    url(
        r"^api/v1/genres$",
        views.genres.as_view(),
        name="jukebox_api_genres"
    ),
    url(
        r"^api/v1/years$",
        views.years.as_view(),
        name="jukebox_api_years"
    ),
    url(
        r"^api/v1/history$",
        views.history.as_view(),
        name="jukebox_api_history"
    ),
    url(
        r"^api/v1/favourites$",
        views.favourites.as_view(),
        name="jukebox_api_favourites"
    ),
    url(
        r"^api/v1/favourites/(?P<song_id>[0-9]+)$",
        views.favourites_item.as_view(),
        name="jukebox_api_favourites_item"
    ),

    url(
        r"^api/v1/queue$",
        views.queue.as_view(),
        name="jukebox_api_queue"
    ),
    url(
        r"^api/v1/queue/(?P<song_id>[0-9]+)$",
        views.queue_item.as_view(),
        name="jukebox_api_queue_item"
    ),
    url(
        r"^api/v1/ping$",
        views.ping.as_view(),
        name="jukebox_api_ping"
    ),
)
