# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import patterns, url
import views

js_info_dict = {
    'packages': (
        'jukebox_web',
    ),
}

urlpatterns = patterns("",
    url(r"^$", views.index, name="jukebox_web_index"),
    url(r"^login$", views.login, name="jukebox_web_login"),
    url(r"^login/error$", views.login_error, name="jukebox_web_login_error"),
    url(
        r"^language/set/(?P<language>[a-z]{2})",
        views.language,
        name="jukebox_web_language"
    ),
    url(r"^logout$", views.logout, name="jukebox_web_logout"),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)
