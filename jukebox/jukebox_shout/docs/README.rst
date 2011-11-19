Jukebox shoutcast streaming
============================

jukebox_shout provides a daemon to stream your music to a shoutcast compatible server like `icecast <http://www.icecast.org>`_

Basic setup instructions for icecast can be found in their `documentation <http://www.icecast.org/docs/icecast-2.3.2/icecast2_basicsetup.html>`_

**Required system libraries**

libshout3, libshout3-dev and python-dev are required to build the dependecy `python-shout <http://pypi.python.org/pypi/python-shout>`_.

Startup
========

::

    bin/jukebox jukebox_shout --start --host=[shoutcast_host] --port[shoutcast_port] --password=[shoutcast_source_password]

Stop
=====

::

    bin/jukebox jukebox_shout --stop

