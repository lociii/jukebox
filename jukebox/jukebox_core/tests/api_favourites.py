# -*- coding: UTF-8 -*-

import simplejson
from jukebox_core.tests.api import ApiTestBase


class ApiFavouritesTest(ApiTestBase):
    def testIndexEmpty(self):
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/favourites"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 0)

    def testAdd(self):
        artist = self.addArtist()
        song = self.addSong(artist)

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

        # check that song is a favourite
        result = simplejson.loads(
            self.httpGet(
                "/api/v1/songs"
            ).content
        )
        self.assertEquals(len(result["itemList"]), 1)
        self.assertEquals(result["itemList"][0]["id"], song.id)
        self.assertTrue(result["itemList"][0]["favourite"])

