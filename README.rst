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

Install `virtualenvwrapper <https://pypi.python.org/pypi/virtualenvwrapper>`_ via `pip <http://pypi.python.org/pypi/pip>`_ if not alreay done:

::

    sudo pip install virtualenvwrapper

Set up a project for jukebox:

::

    mkproject jukebox

Install the jukebox in your fresh virtual environment:

::

    workon jukebox
    pip install jukebox

Now it's time to configure the jukebox

1. Enter admin credentials and select authentication providers
2. Create the database
3. Index your music

That's all

::

    jukebox jukebox_setup
    jukebox syncdb
    jukebox migrate
    jukebox jukebox_index --path=/path/to/library

The django builtin development webserver will be sufficient to serve your office or party. Just start it up:

::

    jukebox runserver ip:port

Now you're ready to put music in the queue.

Playback
=========

Currently there are two methods of playing the music chosen in jukebox.

**shoutcast**

Stream your music to a shoutcast compatible server

::

    pip install jukebox-shout

See `jukebox_shout <https://github.com/lociii/jukebox_shout>`_ for details and startup command.

**mpg123**

Play your music locally on the machine running the jukebox.

::

    pip install jukebox-mpg123

See `jukebox_mpg123 <https://github.com/lociii/jukebox_mpg123>`_ for details and startup command.

**Contribute!**

Feel free to write additional playback modules and I'll add them to the list above.

Live indexing
===============

There is no need to update your index every time a new song is added to your library, just use the live indexer package.

::

    pip install jukebox-live-indexer

See `jukebox_live_indexer <https://github.com/lociii/jukebox_live_indexer>`_ for details and startup command.

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

License
========

MIT License. See `License <https://github.com/lociii/jukebox/blob/master/LICENSE.rst>`_

Contribute!
============

You want to contribute to this project? Just fork the repo and do this:

::

    mkproject jukebox
    git clone git@github.com:[username]/jukebox.git .
    git remote add upstream git://github.com/lociii/jukebox.git
    pip install -r requirements.txt
    cd jukebox

Follow up configuring jukebox like described in Setup. Use ./manage.py instead of the jukebox command.

You can now create a branch to make your actual changes and send a pull request. See `this article <https://www.openshift.com/wiki/github-workflow-for-submitting-pull-requests>`_ for how to do this.

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

0.3.0

- Added jukebox_watch
- Added list of voters
- Minor improvements

0.3.1

- Improved exception handling
- Added rss for current song
- Minor bug fixes

0.3.2

- Update dependencies
- Fix authentication problems
- Switch from inotify to watchdog

0.3.3

- Fix manifest

0.3.4

- Fix to skip unauthorized sessions
- Updated wsgi handler

0.3.5

- Update mutagen (Thanks guys for removing old packages)
- Fixed minor bugs (Thanks to `saz <https://github.com/saz/>`_)

0.3.7

- Fix buggy pypi package

0.4.0

- Split jukebox in different packages
- Strip artist from album data

0.4.1

- Add missing wsgi file
