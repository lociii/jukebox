# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand
from optparse import make_option
import unicodedata
import shout
import daemon
import daemon.pidfile
from signal import SIGTSTP
import sys, os
import jukebox_core.api


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "--start",
            action="store_true",
            dest="start",
            help="Start shoutcast streaming"
        ),
        make_option(
            "--stop",
            action="store_true",
            dest="stop",
            help="Stop shoutcast streaming"
        ),
        make_option(
            "--host",
            action="store",
            dest="host",
            help="Host of shoutcast server"
        ),
        make_option(
            "--port",
            action="store",
            dest="port",
            help="Port of shoutcast server"
        ),
        make_option(
            "--password",
            action="store",
            dest="password",
            help="Source password of shoutcast server"
        ),
    )

    def handle(self, *args, **options):
        pidFile = os.path.dirname(
            os.path.abspath(__file__)
        ) + "/../../daemon.pid"

        if options["start"]:
            if (options["host"] is None or
                options["port"] is None or
                options["password"] is None
            ):
                print "Required arguments: host, port, password"
                self.print_help("jukebox_shout", "help")
                return

            if os.path.exists(pidFile):
                print "Daemon already running, pid file exists"
                return

            pid = daemon.pidfile.TimeoutPIDLockFile(
                pidFile,
                10
            )

            print "Starting jukebox_shout daemon..."
            self.daemon = daemon.DaemonContext(
                uid=os.getuid(),
                gid=os.getgid(),
                pidfile=pid,
                working_directory=os.getcwd(),
                detach_process=True,
                signal_map={
                    SIGTSTP: self.shutdown
                }
            )

            with self.daemon:
                self.stream(
                    channel_mount="/stream",
                    station_url="http://" + options["host"],
                    genre="Mixed",
                    name="Jukebox radio",
                    description="Jukebox - your democratic music player",
                    hostname=options["host"],
                    port=int(options["port"]),
                    password=options["password"],
                )
        elif options["stop"]:
            if not os.path.exists(pidFile):
                print "Daemon not running"
                return

            print "Stopping daemon..."
            pid = int(open(pidFile).read())
            os.kill(pid, SIGTSTP)
        else:
            self.print_help("jukebox_shout", "help")

    def shutdown(self, signal, action):
        self.daemon.close()
        sys.exit(0)

    def stream(
        self,
        channel_mount,
        station_url,
        genre, name,
        description,
        hostname,
        port,
        password
    ):
        self.shout = shout.Shout()
        print "Using libshout version %s" % shout.version()

        self.shout.audio_info = {
            shout.SHOUT_AI_BITRATE: "128",
            shout.SHOUT_AI_SAMPLERATE: "44100",
            shout.SHOUT_AI_CHANNELS: "2"
        }
        self.shout.name = name
        self.shout.url = station_url
        self.shout.mount = channel_mount
        self.shout.port = port
        self.shout.user = "source"
        self.shout.password = password
        self.shout.genre = genre
        self.shout.description = description
        self.shout.host = hostname
        self.shout.ogv = 0
        self.shout.format = "mp3"
        self.shout.open()

        songs_api = jukebox_core.api.songs()
        while 1:
            self.sendfile(songs_api.getNextSong())


    def sendfile(self, song_instance):
        if not os.path.exists(song_instance.Filename):
            print "File not found: %s" %  song_instance.Filename
            return

        print "Streaming file %s" % song_instance.Filename
        f = open(song_instance.Filename)
        self.shout.set_metadata({"song": self.getMetaData(song_instance)})
        nbuf = f.read(4096)
        while 1:
            buf = nbuf
            nbuf = f.read(4096)
            if not len(buf):
                break
            self.shout.send(buf)
            self.shout.sync()
        f.close()

    def getMetaData(self, song_instance):
        return unicodedata.normalize(
            "NFKD",
            song_instance.Artist.Name
        ).encode(
            "ascii",
            "ignore"
        ) + " - " + unicodedata.normalize(
            "NFKD",
            song_instance.Title
        ).encode(
            "ascii",
            "ignore"
        )
