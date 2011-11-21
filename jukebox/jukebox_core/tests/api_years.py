# -*- coding: UTF-8 -*-

import simplejson
from jukebox_core.tests.api import ApiTestBase


class ApiYearsTest(ApiTestBase):
    def testIndexEmpty(self):
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/years"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 0)

    def testIndex(self):
        year = 2000
        self.addSong(artist=self.addArtist(), year=year)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/years"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["year"], year)

    def testIndexOrderBy(self):
        year_a = 2000
        year_b = 2010
        self.addSong(artist=self.addArtist(), year=year_a)
        self.addSong(artist=self.addArtist(), year=year_b)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/years?order_by=year"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["year"], year_a)
        self.assertEquals(result["itemList"][1]["year"], year_b)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/years?order_by=year&order_direction=desc"
            ).content
        )

        self.assertEquals(len(result["itemList"]), 2)
        self.assertEquals(result["itemList"][0]["year"], year_b)
        self.assertEquals(result["itemList"][1]["year"], year_a)

    def testCount(self):
        year_a = 2000
        year_b = 2005
        year_c = 2010
        self.addSong(artist=self.addArtist(), year=year_a)
        self.addSong(artist=self.addArtist(), year=year_b)
        self.addSong(artist=self.addArtist(), year=year_c)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/years?count=1"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["year"], year_a)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/years?count=3"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 3)
        self.assertEquals(result["itemList"][0]["year"], year_a)
        self.assertEquals(result["itemList"][1]["year"], year_b)
        self.assertEquals(result["itemList"][2]["year"], year_c)
        self.assertFalse(result["hasNextPage"])

    def testCountAndPage(self):
        year_a = 2000
        year_b = 2005
        year_c = 2010
        self.addSong(artist=self.addArtist(), year=year_a)
        self.addSong(artist=self.addArtist(), year=year_b)
        self.addSong(artist=self.addArtist(), year=year_c)

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/years?count=1&page=1"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["year"], year_a)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/years?count=1&page=2"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["year"], year_b)
        self.assertTrue(result["hasNextPage"])

        result = simplejson.loads(
            self.httpGet(
                "/api/v1/years?count=1&page=3"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["year"], year_c)
        self.assertFalse(result["hasNextPage"])
