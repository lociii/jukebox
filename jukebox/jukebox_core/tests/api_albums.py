# -*- coding: UTF-8 -*-

import simplejson
from jukebox_core.tests.api import ApiTestBase


class ApiAlbumsTest(ApiTestBase):
    def testIndexEmpty(self):
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/albums"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 0)

    def testIndex(self):
        album = self.addAlbum(artist=self.addArtist())

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/albums"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], album.id)

    def testIndexOrderByAlbum(self):
        album_a = self.addAlbum(artist=self.addArtist(), title="A Title")
        album_b = self.addAlbum(artist=self.addArtist(), title="B Title")

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/albums?order_by=album"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], album_a.id)
        self.assertEquals(result["itemList"][1]["id"], album_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/albums?order_by=album&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], album_b.id)
        self.assertEquals(result["itemList"][1]["id"], album_a.id)

    def testIndexOrderByArtist(self):
        album_a = self.addAlbum(artist=self.addArtist("A Name"))
        album_b = self.addAlbum(artist=self.addArtist("B Name"))

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/albums?order_by=artist"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], album_a.id)
        self.assertEquals(result["itemList"][1]["id"], album_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/albums?order_by=artist&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], album_b.id)
        self.assertEquals(result["itemList"][1]["id"], album_a.id)

    def testCount(self):
        album_a = self.addAlbum(artist=self.addArtist())
        album_b = self.addAlbum(artist=self.addArtist())
        album_c = self.addAlbum(artist=self.addArtist())

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/albums?count=1"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], album_a.id)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/albums?count=3"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 3)
        self.assertEquals(result["itemList"][0]["id"], album_a.id)
        self.assertEquals(result["itemList"][1]["id"], album_b.id)
        self.assertEquals(result["itemList"][2]["id"], album_c.id)
        self.assertFalse(result["hasNextPage"])

    def testCountAndPage(self):
        album_a = self.addAlbum(artist=self.addArtist())
        album_b = self.addAlbum(artist=self.addArtist())
        album_c = self.addAlbum(artist=self.addArtist())

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/albums?count=1&page=1"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], album_a.id)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/albums?count=1&page=2"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], album_b.id)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/albums?count=1&page=3"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], album_c.id)
        self.assertFalse(result["hasNextPage"])
