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
    passwords = {}

    def setUp(self):
        transaction.rollback()

        # register test user and setup auth
        self.user = self.addUser(self.username, self.email, self.password)

    def httpGet(self, url, params={}, user=None):
        c = Client()
        return c.get(url, params, HTTP_AUTHORIZATION=self.getAuth(user))

    def httpPost(self, url, params={}, user=None):
        c = Client()
        return c.post(url, params, HTTP_AUTHORIZATION=self.getAuth(user))

    def httpDelete(self, url, params={}, user=None):
        c = Client()
        return c.delete(url, params, HTTP_AUTHORIZATION=self.getAuth(user))

    def getAuth(self, user=None):
        if user is None:
            user = self.user
        username = user.username
        password = self.passwords[user.id]

        return "Basic %s" % base64.encodestring(
            '%s:%s' % (username, password)
        ).strip()


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
        user = User.objects.create_user(username, email, password)
        self.passwords[user.id] = password
        return user
