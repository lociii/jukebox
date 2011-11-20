# -*- coding: UTF-8 -*-

from django.db import transaction
from jukebox_core.models import Artist, Album, Genre, Song
import random
from jukebox_core.tests import api as apiBase
import jukebox_core.api


class ApiSongsTest(apiBase.ApiTestBase):
    def setUp(self):
        transaction.rollback()

    def testIndex(self):
        artist = self.addArtist()
        song = self.addSong(artist)

        songs_api = jukebox_core.api.songs()
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithSearchTermInTitle(self):
        fixture = "thisIsATestFixtureString"
        fixturePart = fixture[0:random.randint(5, len(fixture))]

        artist = self.addArtist()
        song = self.addSong(artist, None, None, fixture)

        songs_api = jukebox_core.api.songs()
        songs_api.set_search_term(fixturePart)
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithSearchTermInArtistName(self):
        fixture = "thisIsATestFixtureString"
        fixturePart = fixture[0:random.randint(5, len(fixture))]

        artist = self.addArtist(fixture)
        song = self.addSong(artist)

        songs_api = jukebox_core.api.songs()
        songs_api.set_search_term(fixturePart)
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithSearchTermInAlbumTitle(self):
        fixture = "thisIsATestFixtureString"
        fixturePart = fixture[0:random.randint(5, len(fixture))]

        artist = self.addArtist()
        album = self.addAlbum(artist, fixture)
        song = self.addSong(artist, album)

        songs_api = jukebox_core.api.songs()
        songs_api.set_search_term(fixturePart)
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithSearchTitle(self):
        fixture = "thisIsATestFixtureString"
        fixturePart = fixture[0:random.randint(5, len(fixture))]

        artist = self.addArtist()
        song = self.addSong(artist, None, None, fixture)

        songs_api = jukebox_core.api.songs()
        songs_api.set_search_title(fixturePart)
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithSearchArtistName(self):
        fixture = "thisIsATestFixtureString"
        fixturePart = fixture[0:random.randint(5, len(fixture))]

        artist = self.addArtist(fixture)
        song = self.addSong(artist)

        songs_api = jukebox_core.api.songs()
        songs_api.set_search_artist_name(fixturePart)
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithSearchAlbumTitle(self):
        fixture = "thisIsATestFixtureString"
        fixturePart = fixture[0:random.randint(5, len(fixture))]

        artist = self.addArtist()
        album = self.addAlbum(artist, fixture)
        song = self.addSong(artist, album)

        songs_api = jukebox_core.api.songs()
        songs_api.set_search_album_title(fixturePart)
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithFilterYear(self):
        fixture = 2010

        artist = self.addArtist()
        song = self.addSong(artist, None, None, "TestTitle", fixture)

        songs_api = jukebox_core.api.songs()
        songs_api.set_filter_year(fixture)
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithFilterGenre(self):
        artist = self.addArtist()
        genre = self.addGenre()
        song = self.addSong(artist, None, genre)

        songs_api = jukebox_core.api.songs()
        songs_api.set_filter_genre(genre.id)
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithFilterAlbumId(self):
        artist = self.addArtist()
        album = self.addAlbum(artist)
        song = self.addSong(artist, album)

        songs_api = jukebox_core.api.songs()
        songs_api.set_filter_album_id(album.id)
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithFilterArtistId(self):
        artist = self.addArtist()
        song = self.addSong(artist)

        songs_api = jukebox_core.api.songs()
        songs_api.set_filter_artist_id(artist.id)
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexOrderByTitle(self):
        artist = self.addArtist()
        album = self.addAlbum(artist)
        genre = self.addGenre()
        song_a = self.addSong(artist, album, genre, "A Title")
        song_b = self.addSong(artist, album, genre, "B Title")

        songs_api = jukebox_core.api.songs()
        songs_api.set_order_by("title", "asc")
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        songs_api.set_order_by("title", "desc")
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByArtist(self):
        artist_a = self.addArtist("A Name")
        artist_b = self.addArtist("B Name")
        song_a = self.addSong(artist_a)
        song_b = self.addSong(artist_b)

        songs_api = jukebox_core.api.songs()
        songs_api.set_order_by("artist", "asc")
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        songs_api.set_order_by("artist", "desc")
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByAlbum(self):
        artist = self.addArtist()
        album_a = self.addAlbum(artist, "A Title")
        album_b = self.addAlbum(artist, "B Title")
        song_a = self.addSong(artist, album_a)
        song_b = self.addSong(artist, album_b)

        songs_api = jukebox_core.api.songs()
        songs_api.set_order_by("album", "asc")
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        songs_api.set_order_by("album", "desc")
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByYear(self):
        artist = self.addArtist()
        song_a = self.addSong(artist, None, None, "TestTitle", 2000)
        song_b = self.addSong(artist, None, None, "TestTitle", 2001)

        songs_api = jukebox_core.api.songs()
        songs_api.set_order_by("year", "asc")
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        songs_api.set_order_by("year", "desc")
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByGenre(self):
        artist = self.addArtist()
        genre_a = self.addGenre("A Genre")
        genre_b = self.addGenre("B Genre")
        song_a = self.addSong(artist, None, genre_a)
        song_b = self.addSong(artist, None, genre_b)

        songs_api = jukebox_core.api.songs()
        songs_api.set_order_by("genre", "asc")
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        songs_api.set_order_by("genre", "desc")
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByLength(self):
        artist = self.addArtist()
        song_a = self.addSong(artist, None, None, "TestTitle", 2000, 100)
        song_b = self.addSong(artist, None, None, "TestTitle", 2000, 200)

        songs_api = jukebox_core.api.songs()
        songs_api.set_order_by("length", "asc")
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        songs_api.set_order_by("length", "desc")
        result = songs_api.index()

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testGetNextSongRandom(self):
        artist = self.addArtist()
        song = self.addSong(artist, None, None, "TestTitle", 2000, 100, __file__)

        songs_api = jukebox_core.api.songs()
        result = songs_api.getNextSong()

        self.assertEquals(result, song)

        # check if song has been added to history
        history_api = jukebox_core.api.history()
        result = history_api.index()

        self.assertEqual(result["itemList"][0]["id"], song.id)

    def testGetNextSongFromQueue(self):
        artist = self.addArtist()
        song = self.addSong(artist, None, None, "TestTitle", 2000, 100, __file__)

        # add user
        user = self.addUser("testUser", "testPassword")

        # add to queue
        queue_api = jukebox_core.api.queue()
        queue_api.set_user_id(user.id)
        queue_api.add(song.id)

        # get next song
        songs_api = jukebox_core.api.songs()
        result = songs_api.getNextSong()
        self.assertEquals(result, song)

        # check if song has been added to history
        history_api = jukebox_core.api.history()
        result = history_api.index()
        self.assertEqual(result["itemList"][0]["id"], song.id)

        # check if song has been removed from queue
        result = queue_api.index()
        self.assertEqual(len(result["itemList"]), 0)
