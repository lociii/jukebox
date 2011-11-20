# -*- coding: UTF-8 -*-

from django.test import TestCase, Client
from django.db import transaction
import base64
from jukebox_core.models import Artist, Album, Genre, Song
from django.contrib.auth.models import User


class ApiTestBase(TestCase):
    user = None
    username = "TestUser"
    email = "test@domain.org"
    password = "TestPassword"

    def setUp(self):
        transaction.rollback()

        # register test user and setup auth
        self.user = self.addUser(self.username, self.email, self.password)

    def httpGet(self, url, params={}):
        auth = '%s:%s' % (self.username, self.password)
        auth = "Basic %s" % base64.encodestring(auth).strip()
        c = Client()
        return c.get(url, params, HTTP_AUTHORIZATION=auth)

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

    def addUser(self, username, email, password):
        return User.objects.create_user(username, email, password)
