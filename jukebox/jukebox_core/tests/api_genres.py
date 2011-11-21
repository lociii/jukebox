# -*- coding: UTF-8 -*-

import simplejson
from jukebox_core.tests.api import ApiTestBase


class ApiGenresTest(ApiTestBase):
    def testIndexEmpty(self):
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/genres"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 0)

    def testIndex(self):
        genre = self.addGenre()

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/genres"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], genre.id)

    def testIndexOrderBy(self):
        genre_a = self.addGenre(name="A Name")
        genre_b = self.addGenre(name="B Name")

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/genres?order_by=genre"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], genre_a.id)
        self.assertEquals(result["itemList"][1]["id"], genre_b.id)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/genres?order_by=genre&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["id"], genre_b.id)
        self.assertEquals(result["itemList"][1]["id"], genre_a.id)

    def testCount(self):
        genre_a = self.addGenre()
        genre_b = self.addGenre()
        genre_c = self.addGenre()

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/genres?count=1"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], genre_a.id)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/genres?count=3"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 3)
        self.assertEquals(result["itemList"][0]["id"], genre_a.id)
        self.assertEquals(result["itemList"][1]["id"], genre_b.id)
        self.assertEquals(result["itemList"][2]["id"], genre_c.id)
        self.assertFalse(result["hasNextPage"])

    def testCountAndPage(self):
        genre_a = self.addGenre()
        genre_b = self.addGenre()
        genre_c = self.addGenre()

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/genres?count=1&page=1"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], genre_a.id)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/genres?count=1&page=2"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], genre_b.id)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/genres?count=1&page=3"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], genre_c.id)
        self.assertFalse(result["hasNextPage"])
