# -*- coding: UTF-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import api, base64
import forms


class JukeboxAPIView(APIView):
    def api_set_user_id(self, request, api):
        if request.user.is_authenticated():
            api.set_user_id(request.user.id)
        return api


class songs(JukeboxAPIView):
    permissions = (IsAuthenticated, )

    def get(self, request):
        request.session.modified = True

        page = 1
        songs_api = api.songs()
        songs_api = self.api_set_user_id(request, songs_api)

        form = forms.SongsForm(request.GET)
        if form.is_valid():
            if not form.cleaned_data["search_term"] == "":
                songs_api.set_search_term(
                    form.cleaned_data["search_term"]
                )
            if not form.cleaned_data["search_title"] == "":
                songs_api.set_search_title(
                    form.cleaned_data["search_title"]
                )
            if not form.cleaned_data["search_artist"] == "":
                songs_api.set_search_artist_name(
                    form.cleaned_data["search_artist"]
                )
            if not form.cleaned_data["search_album"] == "":
                songs_api.set_search_album_title(
                    form.cleaned_data["search_album"]
                )

            if not form.cleaned_data["filter_artist_id"] is None:
                songs_api.set_filter_artist_id(
                    form.cleaned_data["filter_artist_id"]
                )
            if not form.cleaned_data["filter_album_id"] is None:
                songs_api.set_filter_album_id(
                    form.cleaned_data["filter_album_id"]
                )
            if not form.cleaned_data["filter_genre"] is None:
                songs_api.set_filter_genre(
                    form.cleaned_data["filter_genre"]
                )
            if not form.cleaned_data["filter_year"] is None:
                songs_api.set_filter_year(
                    form.cleaned_data["filter_year"]
                )

            if (not form.cleaned_data["order_by"] == "" and
                not form.cleaned_data["order_direction"] == ""):
                songs_api.set_order_by(
                    form.cleaned_data["order_by"],
                    form.cleaned_data["order_direction"]
                )
            elif not form.cleaned_data["order_by"] == "":
                songs_api.set_order_by(form.cleaned_data["order_by"])

            if not form.cleaned_data["count"] is None:
                songs_api.set_count(form.cleaned_data["count"])
            if not form.cleaned_data["page"] is None:
                page = form.cleaned_data["page"]

        result = songs_api.index(page)
        result["form"] = form.cleaned_data
        return Response(
            data=result
        )


class songs_current(JukeboxAPIView):
    permissions = (IsAuthenticated, )

    def get(self, request):
        request.session.modified = True

        history = api.history()
        current = {}
        try:
            current = history.getCurrent()
        except:
            pass

        return Response(
            data=current
        )


class songs_skip(JukeboxAPIView):
    permissions = (IsAuthenticated, )

    def get(self, request):
        request.session.modified = True

        songs_api = api.songs()
        songs_api.skipCurrentSong()


class artists(JukeboxAPIView):
    permissions = (IsAuthenticated, )

    def get(self, request):
        request.session.modified = True

        page = 1
        artists_api = api.artists()

        form = forms.ArtistsForm(request.GET)
        if form.is_valid():
            if (not form.cleaned_data["order_by"] == "" and
                not form.cleaned_data["order_direction"] == ""):
                artists_api.set_order_by(
                    form.cleaned_data["order_by"],
                    form.cleaned_data["order_direction"]
                )
            elif not form.cleaned_data["order_by"] == "":
                artists_api.set_order_by(form.cleaned_data["order_by"])

            if not form.cleaned_data["count"] is None:
                artists_api.set_count(form.cleaned_data["count"])
            if not form.cleaned_data["page"] is None:
                page = form.cleaned_data["page"]

        return Response(
            data=artists_api.index(page)
        )


class albums(JukeboxAPIView):
    permissions = (IsAuthenticated, )

    def get(self, request):
        request.session.modified = True

        page = 1
        albums_api = api.albums()

        form = forms.AlbumsForm(request.GET)
        if form.is_valid():
            if (not form.cleaned_data["order_by"] == "" and
                not form.cleaned_data["order_direction"] == ""):
                albums_api.set_order_by(
                    form.cleaned_data["order_by"],
                    form.cleaned_data["order_direction"]
                )
            elif not form.cleaned_data["order_by"] == "":
                albums_api.set_order_by(form.cleaned_data["order_by"])

            if not form.cleaned_data["count"] is None:
                albums_api.set_count(form.cleaned_data["count"])
            if not form.cleaned_data["page"] is None:
                page = form.cleaned_data["page"]

        return Response(
            data=albums_api.index(page)
        )


class genres(JukeboxAPIView):
    permissions = (IsAuthenticated, )

    def get(self, request):
        request.session.modified = True

        page = 1
        genres_api = api.genres()

        form = forms.GenresForm(request.GET)
        if form.is_valid():
            if (not form.cleaned_data["order_by"] == "" and
                not form.cleaned_data["order_direction"] == ""):
                genres_api.set_order_by(
                    form.cleaned_data["order_by"],
                    form.cleaned_data["order_direction"]
                )
            elif not form.cleaned_data["order_by"] == "":
                genres_api.set_order_by(form.cleaned_data["order_by"])

            if not form.cleaned_data["count"] is None:
                genres_api.set_count(form.cleaned_data["count"])
            if not form.cleaned_data["page"] is None:
                page = form.cleaned_data["page"]

        return Response(
            data=genres_api.index(page)
        )


class years(JukeboxAPIView):
    permissions = (IsAuthenticated, )

    def get(self, request):
        request.session.modified = True

        page = 1
        years_api = api.years()

        form = forms.YearsForm(request.GET)
        if form.is_valid():
            if (not form.cleaned_data["order_by"] == "" and
                not form.cleaned_data["order_direction"] == ""):
                years_api.set_order_by(
                    form.cleaned_data["order_by"],
                    form.cleaned_data["order_direction"]
                )
            elif not form.cleaned_data["order_by"] == "":
                years_api.set_order_by(form.cleaned_data["order_by"])

            if not form.cleaned_data["count"] is None:
                years_api.set_count(form.cleaned_data["count"])
            if not form.cleaned_data["page"] is None:
                page = form.cleaned_data["page"]

        return Response(
            data=years_api.index(page)
        )


class history(JukeboxAPIView):
    permissions = (IsAuthenticated, )

    def get(self, request):
        request.session.modified = True

        page = 1
        history_api = api.history()
        history_api = self.api_set_user_id(request, history_api)

        form = forms.HistoryForm(request.GET)
        if form.is_valid():
            if (not form.cleaned_data["order_by"] == "" and
                not form.cleaned_data["order_direction"] == ""):
                history_api.set_order_by(
                    form.cleaned_data["order_by"],
                    form.cleaned_data["order_direction"]
                )
            elif not form.cleaned_data["order_by"] == "":
                history_api.set_order_by(form.cleaned_data["order_by"])

            if not form.cleaned_data["count"] is None:
                history_api.set_count(form.cleaned_data["count"])
            if not form.cleaned_data["page"] is None:
                page = form.cleaned_data["page"]

        return Response(
            data=history_api.index(page)
        )


class history_my(JukeboxAPIView):
    permissions = (IsAuthenticated, )

    def get(self, request):
        request.session.modified = True

        page = 1
        history_api = api.history_my()
        history_api = self.api_set_user_id(request, history_api)

        form = forms.HistoryForm(request.GET)
        if form.is_valid():
            if (not form.cleaned_data["order_by"] == "" and
                not form.cleaned_data["order_direction"] == ""):
                history_api.set_order_by(
                    form.cleaned_data["order_by"],
                    form.cleaned_data["order_direction"]
                )
            elif not form.cleaned_data["order_by"] == "":
                history_api.set_order_by(form.cleaned_data["order_by"])

            if not form.cleaned_data["count"] is None:
                history_api.set_count(form.cleaned_data["count"])
            if not form.cleaned_data["page"] is None:
                page = form.cleaned_data["page"]

        return Response(
            data=history_api.index(page)
        )


class queue(JukeboxAPIView):
    permissions = (IsAuthenticated, )
    form = forms.IdForm

    def get(self, request):
        request.session.modified = True

        page = 1
        queue_api = api.queue()
        queue_api = self.api_set_user_id(request, queue_api)

        form = forms.QueueForm(request.GET)
        if form.is_valid():
            if (not form.cleaned_data["order_by"] == "" and
                not form.cleaned_data["order_direction"] == ""):
                queue_api.set_order_by(
                    form.cleaned_data["order_by"],
                    form.cleaned_data["order_direction"]
                )
            elif not form.cleaned_data["order_by"] == "":
                queue_api.set_order_by(form.cleaned_data["order_by"])

            if not form.cleaned_data["count"] is None:
                queue_api.set_count(form.cleaned_data["count"])
            if not form.cleaned_data["page"] is None:
                page = form.cleaned_data["page"]

        result = queue_api.index(page)
        for k, v in enumerate(result["itemList"]):
            result["itemList"][k]["url"] = reverse(
                "jukebox_api_queue_item",
                kwargs={"song_id": v["id"]}
            )
        return Response(
            data=result
        )

    def post(self, request):
        request.session.modified = True

        queue_api = api.queue()
        queue_api = self.api_set_user_id(request, queue_api)

        try:
            song_id = queue_api.add(self.request.POST["id"])
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    'id': int(self.request.POST['id'])
                },
                headers={"Location": reverse(
                    "jukebox_api_queue_item",
                    kwargs={"song_id": song_id}
                )}
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception, e:
            print e
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class queue_item(JukeboxAPIView):
    permissions = (IsAuthenticated, )
    form = forms.IdForm

    def get(self, request, song_id):
        request.session.modified = True

        queue_api = api.queue()
        queue_api = self.api_set_user_id(request, queue_api)

        try:
            item = queue_api.get(song_id)
            item["url"] = reverse(
                "jukebox_api_queue_item",
                kwargs={"song_id": item["id"]}
            )
            return Response(
                data=item
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception, e:
            print e
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, song_id):
        request.session.modified = True

        queue_api = api.queue()
        queue_api = self.api_set_user_id(request, queue_api)

        try:
            return Response(
                data=queue_api.remove(song_id)
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class favourites(JukeboxAPIView):
    permissions = (IsAuthenticated, )
    form = forms.IdForm

    def get(self, request):
        request.session.modified = True

        page = 1
        favourites_api = api.favourites()
        favourites_api = self.api_set_user_id(request, favourites_api)

        form = forms.FavouritesForm(request.GET)
        if form.is_valid():
            if (not form.cleaned_data["order_by"] == "" and
                not form.cleaned_data["order_direction"] == ""):
                favourites_api.set_order_by(
                    form.cleaned_data["order_by"],
                    form.cleaned_data["order_direction"]
                )
            elif not form.cleaned_data["order_by"] == "":
                favourites_api.set_order_by(form.cleaned_data["order_by"])

            if not form.cleaned_data["count"] is None:
                favourites_api.set_count(form.cleaned_data["count"])
            if not form.cleaned_data["page"] is None:
                page = form.cleaned_data["page"]

        result = favourites_api.index(page)
        for k, v in enumerate(result["itemList"]):
            result["itemList"][k]["url"] = reverse(
                "jukebox_api_favourites_item",
                kwargs={"song_id": v["id"]}
            )
        return Response(
            data=result
        )

    def post(self, request):
        request.session.modified = True

        favourites_api = api.favourites()
        favourites_api = self.api_set_user_id(request, favourites_api)

        try:
            song_id = favourites_api.add(self.request.POST["id"])
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    'id': int(self.request.POST['id']),
                },
                headers={"Location": reverse(
                    "jukebox_api_favourites_item",
                    kwargs={"song_id": song_id}
                )}
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception, e:
            print e
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class favourites_item(JukeboxAPIView):
    permissions = (IsAuthenticated, )
    form = forms.IdForm

    def get(self, request, song_id):
        request.session.modified = True

        favourites_api = api.favourites()
        favourites_api = self.api_set_user_id(request, favourites_api)

        try:
            item = favourites_api.get(song_id)
            item["url"] = reverse(
                "jukebox_api_favourites_item",
                kwargs={"song_id": item["id"]}
            )
            return Response(
                data=item
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception, e:
            print e
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, song_id):
        request.session.modified = True

        favourites_api = api.favourites()
        favourites_api = self.api_set_user_id(request, favourites_api)

        try:
            return Response(
                data=favourites_api.remove(song_id)
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception, e:
            print e
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ping(JukeboxAPIView):
    def get(self, request):
        request.session.modified = True
        return Response(
            data= {
                "ping": True
            }
        )
