# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand
from optparse import make_option
import os
import sys
import daemon
import daemon.pidfile
from signal import SIGTSTP
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from jukebox.jukebox_core.management.commands.jukebox_index import FileIndexer


class EventHandler(FileSystemEventHandler):
    def __init__(self):
        self.indexer = FileIndexer()

    def on_created(self, event):
        if not event.is_directory:
            if os.path.splitext(event.src_path)[-1].lower() == ".mp3":
                self.indexer.index(event.src_path)

    def on_modified(self, event):
        self.on_created(event)


class Command(BaseCommand):
    monitor = None

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
            handler = EventHandler()

            self.monitor = Observer()
            self.monitor.schedule(handler, path, recursive=True)
            self.monitor.run()

    def shutdown(self, signal, action):
        if self.monitor is not None:
            self.monitor.stop()
        self.daemon.close()
        sys.exit(0)
