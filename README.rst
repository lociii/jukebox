Democratic Jukebox - your democratic music player
==================================================

Ever wanted to listen to music with a larger group of people e.g. in your office? Who decides what to play?
Make your music player democratic and give everyone the chance to promote their favourite song.

Jukebox provides a web interface to search your music library and vote for songs to be played.
The more votes a song gets, the sooner you will listen to it.

At one point in your life your play queue might get empty. Don't worry, the jukebox will keep on playing.
The playback system figures out who is online using the web interface or API and plays music to their liking.

**Required system libraries**

libshout3, libshout3-dev and python-dev are required to build the dependecy `python-shout <http://pypi.python.org/pypi/python-shout>`_.

.. image:: http://static.jensnistler.de/jukebox.png
   :height: 404px
   :width: 872px
   :scale: 100%
   :alt: Democratic Jukebox - your democratic music player

General
========

- Jukebox is available in english and german
- Jukebox uses Facebook, Twitter and Github for authentication (see `django-social-auth <https://github.com/omab/django-social-auth>`_ for more authentication providers)

Setup
==================

Install `virtualenv <http://pypi.python.org/pypi/virtualenv>`_ via `pip <http://pypi.python.org/pypi/pip>`_ if not alreay done:

::

    sudo pip install virtualenv

Set up a virtualenv for jukebox:

::

    virtualenv --no-site-packages jukebox

Install ez_setup and finally jukebox in your fresh virtual environment:

::

    cd jukebox
    bin/pip install ez_setup
    bin/pip install jukebox

Now it's time to configure the jukebox

1. Enter admin credentials and select authentication providers
2. Create the database
3. Index your music

That's all

::

    bin/jukebox jukebox_setup
    bin/jukebox syncdb
    bin/jukebox jukebox_index --path=/path/to/library

The django builtin development webserver will be sufficient to serve your office or party. Just start it up:

::

    bin/jukebox runserver ip:port

Now you're ready to put music in the queue. Jukebox offers several methods to play it:

**shoutcast**

See `jukebox_shout <https://github.com/lociii/jukebox/blob/master/jukebox/jukebox_shout/docs/README.rst>`_

**mpg123**

See `jukebox_mpg123 <https://github.com/lociii/jukebox/blob/master/jukebox/jukebox_mpg123/docs/README.rst>`_

Feel free to fork jukebox and add additional playback modules.

API
=============

jukebox_core provides a fully fledged REST API for authenticated users. See `API reference <https://github.com/lociii/jukebox/blob/master/jukebox/jukebox_core/docs/API.rst>`_

Search filters
===============

Jukebox supports google-like search filter. Available search fields: title, artist, album, genre, year.

::

    title:(love to dance) artist:bobby
    artist:(bobby baby) lucky
    title:(in ten years) genre:electronic

Dependencies
=============

::

    Django==1.3
    mutagen==1.20
    django-social-auth==0.6.0
    djangorestframework==0.2.3
    python-shout==0.2
    python-daemon==1.6

License
========

MIT License. See `License <https://github.com/lociii/jukebox/blob/master/LICENSE.rst>`_

Developers
===========

Clone the git repository, change directory to jukebox/jukebox/ and replace the calls to "bin/jukebox" by "python manage.py"

Release Notes
==============

0.1.0

- Initial release

0.1.1

- Fixed installer bugs
- Added personal history
- Added system tests for api

0.2.0

- Language switch
- Sortable lists
- Google-like search operators
- Autoplay tries to play appropriate music
- Improved web interface

0.2.1

- fixed issue with autoplay
