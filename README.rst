Jukebox - your democratic media player
=======================================

Ever wanted to listen to music with a larger group of people e.g. in your office? Who decides what to play?
Make your music player democratic and give everyone the chance to promote their favourite song.

Jukebox provides a web interface to search your music library and vote for songs to be played.
The more votes a song gets, the sooner you will listen to it.

**Required system libraries**

libshout3, libshout3-dev and python-dev are required to build the dependecy `python-shout <http://pypi.python.org/pypi/python-shout>`_.

.. image:: http://static.jensnistler.de/jukebox.png
   :height: 404px
   :width: 872px
   :scale: 100%
   :alt: Jukebox - your democratic media player
   :align: center

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

jukebox_core provides a fully fledged REST API. See `API reference <https://github.com/lociii/jukebox/blob/master/jukebox/jukebox_core/docs/API.rst>`_

Dependencies
=============

::

    Django==1.3
    mutagen==1.20
    django-social-auth==0.6.0
    djangorestframework==0.2.3
    python-shout==0.2

License
========

MIT License. See `License <https://github.com/lociii/jukebox/blob/master/LICENSE.rst>`_

Release Notes
==============

0.1.0
- Initial release
