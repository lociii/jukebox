# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand
from optparse import make_option
import daemon
import daemon.pidfile
from signal import SIGTSTP, SIGTERM
import sys, os, subprocess
import time
import jukebox_core.api


class Command(BaseCommand):
    daemon = None
    proc = None
    mpg123 = None

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
    )

    def handle(self, *args, **options):
        # check if mpg123 is available
        fin, fout = os.popen4(["which", "mpg123"])
        self.mpg123 = fout.read().replace("\n", "")
        if not len(self.mpg123):
            print "mpg123 not installed"
            return

        pidFile = os.path.dirname(
            os.path.abspath(__file__)
        ) + "/../../daemon.pid"

        if options["start"]:
            if os.path.exists(pidFile):
                print "Daemon already running, pid file exists"
                return

            pid = daemon.pidfile.TimeoutPIDLockFile(
                pidFile,
                10
            )

            print "Starting jukebox_mpg123 daemon..."
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
                self.play()

        elif options["stop"]:
            if not os.path.exists(pidFile):
                print "Daemon not running"
                return

            print "Stopping daemon..."
            pid = int(open(pidFile).read())
            os.kill(pid, SIGTSTP)
        else:
            self.print_help("jukebox_shout", "help")

    def play(self):
        songs_api = jukebox_core.api.songs()
        while 1:
            if self.proc is None:
                song_instance = songs_api.getNextSong()

                if not os.path.exists(song_instance.Filename):
                    print "File not found: %s" %  song_instance.Filename
                    continue

                print "Playing " + song_instance.Filename
                self.proc = subprocess.Popen(
                    [self.mpg123, song_instance.Filename]
                )
            else:
                if not self.proc.poll() is None:
                    self.proc = None
            time.sleep(0.5)

    def shutdown(self, signal, action):
        if not self.proc is None:
            os.kill(self.proc.pid, SIGTERM)

        if not self.daemon is None:
            self.daemon.close()
        sys.exit(0)
