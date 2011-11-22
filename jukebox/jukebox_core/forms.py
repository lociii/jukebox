# -*- coding: UTF-8 -*-

from django import forms


class IdForm(forms.Form):
    id = forms.IntegerField(
        required=True
    )


class SongsForm(forms.Form):
    count = forms.IntegerField(
        required=False
    )
    page = forms.IntegerField(
        required=False
    )

    search_term = forms.CharField(
        required=False
    )
    search_title = forms.CharField(
        required=False
    )
    search_artist = forms.CharField(
        required=False
    )
    search_album = forms.CharField(
        required=False
    )

    filter_year = forms.IntegerField(
        required=False
    )
    filter_genre = forms.IntegerField(
        required=False
    )
    filter_album_id = forms.IntegerField(
        required=False
    )
    filter_artist_id = forms.IntegerField(
        required=False
    )

    order_by = forms.CharField(
        max_length=6,
        help_text="'title', 'artist', 'album', 'year', 'genre'",
        required=False
    )
    order_direction = forms.CharField(
        max_length=4,
        help_text="'asc', 'desc'",
        required=False
    )


class ArtistsForm(forms.Form):
    count = forms.IntegerField(
        required=False
    )
    page = forms.IntegerField(
        required=False
    )

    order_by = forms.CharField(
        max_length=6,
        help_text="'artist'",
        required=False
    )
    order_direction = forms.CharField(
        max_length=4,
        help_text="'asc', 'desc'",
        required=False
    )


class AlbumsForm(forms.Form):
    count = forms.IntegerField(
        required=False
    )
    page = forms.IntegerField(
        required=False
    )

    order_by = forms.CharField(
        max_length=6,
        help_text="'album', 'artist'",
        required=False
    )
    order_direction = forms.CharField(
        max_length=4,
        help_text="'asc', 'desc'",
        required=False
    )


class GenresForm(forms.Form):
    count = forms.IntegerField(
        required=False
    )
    page = forms.IntegerField(
        required=False
    )

    order_by = forms.CharField(
        max_length=5,
        help_text="'genre'",
        required=False
    )
    order_direction = forms.CharField(
        max_length=4,
        help_text="'asc', 'desc'",
        required=False
    )


class YearsForm(forms.Form):
    count = forms.IntegerField(
        required=False
    )
    page = forms.IntegerField(
        required=False
    )

    order_by = forms.CharField(
        max_length=4,
        help_text="'year'",
        required=False
    )
    order_direction = forms.CharField(
        max_length=4,
        help_text="'asc', 'desc'",
        required=False
    )


class HistoryForm(forms.Form):
    count = forms.IntegerField(
        required=False
    )
    page = forms.IntegerField(
        required=False
    )

    order_by = forms.CharField(
        max_length=7,
        help_text="'title', 'artist', 'album', 'year', 'genre', 'created'",
        required=False
    )
    order_direction = forms.CharField(
        max_length=4,
        help_text="'asc', 'desc'",
        required=False
    )


class FavouritesForm(forms.Form):
    count = forms.IntegerField(
        required=False
    )
    page = forms.IntegerField(
        required=False
    )

    order_by = forms.CharField(
        max_length=7,
        help_text="'title', 'artist', 'album', 'year', 'genre', 'created'",
        required=False
    )
    order_direction = forms.CharField(
        max_length=4,
        help_text="'asc', 'desc'",
        required=False
    )


class QueueForm(forms.Form):
    count = forms.IntegerField(
        required=False
    )
    page = forms.IntegerField(
        required=False
    )

    order_by = forms.CharField(
        max_length=7,
        help_text="'title', 'artist', 'album', 'year', \
            'genre', 'created', 'votes'",
        required=False
    )
    order_direction = forms.CharField(
        max_length=4,
        help_text="'asc', 'desc'",
        required=False
    )
