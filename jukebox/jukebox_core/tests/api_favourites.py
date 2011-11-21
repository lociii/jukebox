# -*- coding: UTF-8 -*-

import simplejson
from jukebox_core.tests.api import ApiTestBase

# ATTENTION: order tests
# favourites are ordered by insertion date DESC per default
class ApiFavouritesTest(ApiTestBase):
    def testIndexEmpty(self):
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 0)

    def testAddAndIndex(self):
        # register second user
        user = self.addUser("TestUser2", "test2@domain.org", "TestPassword2")

        song = self.addSong(artist=self.addArtist())

        # check that song is not a favourite
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)
        self.assertFalse(result["itemList"][0]["favourite"])

        # add to favourites
        response = self.httpPost(
            "/api/v1/favourites",
            {"id": song.id}
        )
        content = simplejson.loads(
            response.content
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(content["id"], song.id)

        # check favourites list
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

        # check that song is marked as favourite
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)
        self.assertTrue(result["itemList"][0]["favourite"])

        # check favourites list of second user
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites",
                {},
                user
            ).content
        )
        self.assertEquals(len(result["itemList"]), 0)

        # check that song is not marked as favourite for second user
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs",
                {},
                user
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)
        self.assertFalse(result["itemList"][0]["favourite"])

    def testDeleteAndIndex(self):
        song = self.addSong(artist=self.addArtist())

        # add to favourites
        response = self.httpPost(
            "/api/v1/favourites",
            {"id": song.id}
        )
        content = simplejson.loads(
            response.content
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(content["id"], song.id)

        # check favourites list
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)

        # remove from favourites
        response = self.httpDelete(
            "/api/v1/favourites/" + str(song.id),
        )
        content = simplejson.loads(
            response.content
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["id"], str(song.id))

        # check favourites list
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 0)

    def addFavourite(self, song):
        return self.httpPost(
            "/api/v1/favourites",
            {"id": song.id}
        )

    def testIndexOrderByTitle(self):
        song_a = self.addSong(artist=self.addArtist(), title="A Title")
        song_b = self.addSong(artist=self.addArtist(), title="B Title")
        self.addFavourite(song_a)
        self.addFavourite(song_b)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?order_by=title"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?order_by=title&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByArtist(self):
        song_a = self.addSong(artist=self.addArtist(name="A Name"))
        song_b = self.addSong(artist=self.addArtist(name="B Name"))
        self.addFavourite(song_a)
        self.addFavourite(song_b)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?order_by=artist"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?order_by=artist&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByAlbum(self):
        album_a = self.addAlbum(artist=self.addArtist(), title="A Title")
        album_b = self.addAlbum(artist=self.addArtist(), title="B Title")
        song_a = self.addSong(artist=self.addArtist(), album=album_a)
        song_b = self.addSong(artist=self.addArtist(), album=album_b)
        self.addFavourite(song_a)
        self.addFavourite(song_b)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?order_by=album"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?order_by=album&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByYear(self):
        song_a = self.addSong(artist=self.addArtist(), year=2000)
        song_b = self.addSong(artist=self.addArtist(), year=2001)
        self.addFavourite(song_a)
        self.addFavourite(song_b)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?order_by=year"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?order_by=year&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByGenre(self):
        song_a = self.addSong(
            artist=self.addArtist(),
            genre=self.addGenre(name="A Genre")
        )
        song_b = self.addSong(
            artist=self.addArtist(),
            genre=self.addGenre(name="B Genre")
        )
        self.addFavourite(song_a)
        self.addFavourite(song_b)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?order_by=genre"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?order_by=genre&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testIndexOrderByCreated(self):
        song_a = self.addSong(artist=self.addArtist())
        song_b = self.addSong(artist=self.addArtist())
        self.addFavourite(song_a)
        self.addFavourite(song_b)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?order_by=created"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?order_by=created&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertEquals(result["itemList"][1]["id"], song_a.id)

    def testCount(self):
        song_a = self.addSong(artist=self.addArtist())
        song_b = self.addSong(artist=self.addArtist())
        song_c = self.addSong(artist=self.addArtist())
        self.addFavourite(song_a)
        self.addFavourite(song_b)
        self.addFavourite(song_c)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?count=1"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song_c.id)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?count=3"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 3)
        self.assertEquals(result["itemList"][0]["id"], song_c.id)
        self.assertEquals(result["itemList"][1]["id"], song_b.id)
        self.assertEquals(result["itemList"][2]["id"], song_a.id)
        self.assertFalse(result["hasNextPage"])

    def testCountAndPage(self):
        song_a = self.addSong(artist=self.addArtist())
        song_b = self.addSong(artist=self.addArtist())
        song_c = self.addSong(artist=self.addArtist())
        self.addFavourite(song_a)
        self.addFavourite(song_b)
        self.addFavourite(song_c)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?count=1&page=1"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song_c.id)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?count=1&page=2"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song_b.id)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites?count=1&page=3"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song_a.id)
        self.assertFalse(result["hasNextPage"])
