# -*- coding: UTF-8 -*-

from django.test import TestCase
from jukebox_core.models import Artist, Album, Genre, Song
from django.contrib.auth.models import User
import jukebox_core.api


class ApiTestBase(TestCase):
    def addArtist(self, name="TestArist"):
        artist = Artist(
            Name=name
        )
        artist.save()
        return artist

    def addAlbum(self, artist, title="TestTitle"):
        album = Album(
            Artist=artist,
            Title=title
        )
        album.save()
        return album

    def addGenre(self, name="TestGenre"):
        genre = Genre(
            Name=name
        )
        genre.save()
        return genre

    def addSong(
        self,
        artist,
        album = None,
        genre = None,
        title="TestTitle",
        year=2000,
        length=100,
        filename="/path/to/test.mp3"
    ):
        # save a song
        song = Song(
            Artist=artist,
            Album=album,
            Genre=genre,
            Title=title,
            Year=year,
            Length=length,
            Filename=filename
        )
        song.save()
        return song

    def addUser(self, username, password):
        user = User(
            username=username,
            password=password
        )
        user.save()
        return user
