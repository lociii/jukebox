# -*- coding: UTF-8 -*-

import random, simplejson
from jukebox_core import api
from jukebox_core.tests.api import ApiTestBase


class ApiSongsTest(ApiTestBase):
    def testIndexEmpty(self):
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 0)

    def testIndex(self):
        song = self.addSong(artist=self.addArtist())

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithSearchTermInTitle(self):
        fixture = "thisIsATestFixtureString"
        fixturePart = fixture[0:random.randint(5, len(fixture))]

        song = self.addSong(artist=self.addArtist(), title=fixture)
        self.addSong(artist=self.addArtist(), title="AAAAAAAAAAAAAA")

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?search_term=" + fixturePart
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithSearchTermInArtistName(self):
        fixture = "thisIsATestFixtureString"
        fixturePart = fixture[0:random.randint(5, len(fixture))]

        song = self.addSong(artist=self.addArtist(name=fixture))
        self.addSong(artist=self.addArtist(name="AAAAAAAAAAAAAA"))

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?search_term=" + fixturePart
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithSearchTermInAlbumTitle(self):
        fixture = "thisIsATestFixtureString"
        fixturePart = fixture[0:random.randint(5, len(fixture))]

        artist = self.addArtist()
        album = self.addAlbum(artist=artist, title=fixture)
        song = self.addSong(artist=artist, album=album)
        self.addSong(
            artist=artist,
            album=self.addAlbum(artist=artist, title="AAAAAAAAAAAAAA")
        )

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?search_term=" + fixturePart
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithSearchTitle(self):
        fixture = "thisIsATestFixtureString"
        fixturePart = fixture[0:random.randint(5, len(fixture))]

        song = self.addSong(artist=self.addArtist(), title=fixture)
        self.addSong(artist=self.addArtist(), title="AAAAAAAAAAAAAA")

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?search_title=" + fixturePart
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithSearchArtistName(self):
        fixture = "thisIsATestFixtureString"
        fixturePart = fixture[0:random.randint(5, len(fixture))]

        song = self.addSong(artist=self.addArtist(name=fixture))
        self.addSong(artist=self.addArtist(name="AAAAAAAAAAAAAA"))

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?search_artist=" + fixturePart
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithSearchAlbumTitle(self):
        fixture = "thisIsATestFixtureString"
        fixturePart = fixture[0:random.randint(5, len(fixture))]

        artist = self.addArtist()
        album = self.addAlbum(artist=artist, title=fixture)
        song = self.addSong(artist=artist, album=album)
        self.addSong(
            artist=artist,
            album=self.addAlbum(artist=artist, title="AAAAAAAAAAAAAA")
        )

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?search_album=" + fixturePart
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithFilterYear(self):
        fixture = 2010
        song = self.addSong(artist=self.addArtist(), year=fixture)
        self.addSong(artist=self.addArtist(), year=2001)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?filter_year=" + str(fixture)
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithFilterGenre(self):
        genre = self.addGenre()
        song = self.addSong(artist=self.addArtist(), genre=genre)
        self.addSong(artist=self.addArtist(), genre=self.addGenre())

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?filter_genre=" + str(genre.id)
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithFilterAlbumId(self):
        artist = self.addArtist()
        album = self.addAlbum(artist=artist)
        song = self.addSong(artist=artist, album=album)
        self.addSong(artist=artist, album=self.addAlbum(artist=artist))

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?filter_album_id=" + str(album.id)
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexWithFilterArtistId(self):
        artist = self.addArtist()
        song = self.addSong(artist=artist)
        self.addSong(artist=self.addArtist())

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?filter_artist_id=" + str(artist.id)
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

    def testIndexOrderByTitle(self):
        song_a = self.addSong(artist=self.addArtist(), title="A Title")
        song_b = self.addSong(artist=self.addArtist(), title="B Title")

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?order_by=title"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?order_by=title&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByArtist(self):
        song_a = self.addSong(artist=self.addArtist(name="A Name"))
        song_b = self.addSong(artist=self.addArtist(name="B Name"))

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?order_by=artist"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?order_by=artist&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByAlbum(self):
        artist = self.addArtist()
        album_a = self.addAlbum(artist=artist, title="A Title")
        album_b = self.addAlbum(artist=artist, title="B Title")
        song_a = self.addSong(artist=artist, album=album_a)
        song_b = self.addSong(artist=artist, album=album_b)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?order_by=album"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?order_by=album&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByYear(self):
        song_a = self.addSong(artist=self.addArtist(), year=2000)
        song_b = self.addSong(artist=self.addArtist(), year=2001)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?order_by=year"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?order_by=year&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByGenre(self):
        song_a = self.addSong(
            artist=self.addArtist(),
            genre=self.addGenre(name="A Name")
        )
        song_b = self.addSong(
            artist=self.addArtist(),
            genre=self.addGenre(name="B Name")
        )

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?order_by=genre"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?order_by=genre&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByLength(self):
        song_a = self.addSong(artist=self.addArtist(), length=100)
        song_b = self.addSong(artist=self.addArtist(), length=200)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?order_by=length"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?order_by=length&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testCount(self):
        song_a = self.addSong(artist=self.addArtist())
        song_b = self.addSong(artist=self.addArtist())
        song_c = self.addSong(artist=self.addArtist())

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?count=1"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?count=3"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 3)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)
        self.assertEquals(result["itemList"][2]["id"], song_c.id)
        self.assertFalse(result["hasNextPage"])

    def testCountAndPage(self):
        song_a = self.addSong(artist=self.addArtist())
        song_b = self.addSong(artist=self.addArtist())
        song_c = self.addSong(artist=self.addArtist())

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?count=1&page=1"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?count=1&page=2"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs?count=1&page=3"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song_c.id)
        self.assertFalse(result["hasNextPage"])

    def testGetNextSongRandom(self):
        song = self.addSong(artist=self.addArtist(), filename=__file__)

        songs_api = api.songs()
        result = songs_api.getNextSong()

        self.assertEquals(result, song)

        # check if song has been added to history
        history_api = api.history()
        result = history_api.index()

        self.assertEqual(result["itemList"][0]["id"], song.id)

    def testGetNextSongFromQueue(self):
        song = self.addSong(artist=self.addArtist(), filename=__file__)

        # add to queue
        queue_api = api.queue()
        queue_api.set_user_id(self.user.id)
        queue_api.add(song.id)

        # get next song
        songs_api = api.songs()
        result = songs_api.getNextSong()
        self.assertEquals(result, song)

        # check if song has been added to history
        history_api = api.history()
        result = history_api.index()
        self.assertEqual(result["itemList"][0]["id"], song.id)

        # check if song has been removed from queue
        result = queue_api.index()
        self.assertEqual(len(result["itemList"]), 0)
