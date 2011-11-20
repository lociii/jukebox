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
        artist = self.addArtist()
        album = self.addAlbum(artist)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/albums"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], album.id)

    def testIndexOrderBy(self):
        artist = self.addArtist()
        album_a = self.addAlbum(artist, "A Name")
        album_b = self.addAlbum(artist, "B Name")

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

    def testCount(self):
        artist = self.addArtist()
        album_a = self.addAlbum(artist)
        album_b = self.addAlbum(artist)
        album_c = self.addAlbum(artist)

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
        artist = self.addArtist()
        album_a = self.addAlbum(artist)
        album_b = self.addAlbum(artist)
        album_c = self.addAlbum(artist)

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
