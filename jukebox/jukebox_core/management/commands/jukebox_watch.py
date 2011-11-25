# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand
from optparse import make_option
import os, sys
import daemon
import daemon.pidfile
from signal import SIGTSTP
import pyinotify
from jukebox_core.management.commands.jukebox_index import FileIndexer


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self):
        self.indexer = FileIndexer()

    def process_IN_CREATE(self, event):
        if event.pathname.endswith(".mp3"):
            self.indexer.index(event.pathname)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--path",
            action="store",
            dest="path",
            help="Music library path to watch"
        ),
        make_option("--start",
            action="store_true",
            dest="start",
            help="Start watching directory for changes"
        ),
        make_option("--stop",
            action="store_true",
            dest="stop",
            help="Stop watching directory for changes"
        ),
    )

    def handle(self, *args, **options):
        if options["path"] is None:
            print "Required arguments: path"
            return

        if not os.path.exists(options["path"]):
            print "Path does not exist"
            return

        pidFile = os.path.dirname(
            os.path.abspath(__file__)
        ) + "/../../jukebox_watch.pid"

        if options["start"]:
            if os.path.exists(pidFile):
                print "Watch daemon already running, pid file exists"
                return

            self.watch(pidFile, options['path'])
        elif options["stop"]:
            if not os.path.exists(pidFile):
                print "Daemon not running"
                return

            print "Stopping daemon..."
            pid = int(open(pidFile).read())
            os.kill(pid, SIGTSTP)

    def watch(self, pidFile, path):
        pid = daemon.pidfile.TimeoutPIDLockFile(
            pidFile,
            10
        )

        print "Starting jukebox_watch daemon..."
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
            # create watchmanager, eventhandler and notifier
            wm = pyinotify.WatchManager()
            handler = EventHandler()
            self.notifier = pyinotify.Notifier(wm, handler)

            # add watch
            mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE
            wm.add_watch(path, mask, rec=True)
            self.notifier.loop()

    def shutdown(self, signal, action):
        self.notifier.stop()
        self.daemon.close()
        sys.exit(0)
