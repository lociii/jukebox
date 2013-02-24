# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r"^admin/", include(admin.site.urls)),
    url(r"^admin/doc/", include("django.contrib.admindocs.urls")),

    url(r'', include('jukebox.jukebox_web.urls')),
    url(r'', include('jukebox.jukebox_core.urls')),
    url(r'', include('social_auth.urls')),
)
