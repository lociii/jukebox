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

1. Enter admin credentials and select authentication providers
2. Create the database
3. Index your music

That's all

::

    python manage.py jukebox_setup
    python manage.py syncdb
    python manage.py jukebox_index --path=/path/to/library

The django builtin development webserver will be sufficient to serve your office or party. Just start it up:

::

    python manage.py runserver ip:port

Now you're ready to put music in the queue. Jukebox offers several methods to play it:

**shoutcast**

see `jukebox_shout <https://github.com/lociii/jukebox/blob/master/jukebox/jukebox_shout/docs/README.rst>`_

**mpg123**

see `jukebox_mpg123 <https://github.com/lociii/jukebox/blob/master/jukebox/jukebox_mpg123/docs/README.rst>`_

Feel free to fork jukebox and add additional playback modules.

API
=============

The jukebox_core app provides a fully fledged REST API.
API documentation is available here: `API reference <https://github.com/lociii/jukebox/blob/master/jukebox/jukebox_core/docs/API.rst>`_

License
========

MIT License
see `License <https://github.com/lociii/jukebox/blob/master/LICENSE.rst>`_

Release Notes
==============

0.1.0
- Initial release
