# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from optparse import make_option
import os
from jukebox.jukebox_core.utils import FileIndexer


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--path", action="store", dest="path",
                    help="Music library path to scan"),
    )

    def handle(self, *args, **options):
        if options["path"] is None:
            print "Required arguments: path"
            return

        if not os.path.exists(options["path"]):
            print "Path does not exist"
            return

        print "Indexing music in " + options["path"]
        print "This may take a while"
        self.index(options["path"], int(options["verbosity"]))

    def index(self, path, verbosity):
        if not path.endswith("/"):
            path += "/"

        indexer = FileIndexer()

        listing = os.listdir(path)
        for filename in listing:
            filename = path + filename
            if os.path.isdir(filename):
                self.index(filename + "/", verbosity)
            elif filename.endswith(".mp3"):
                if verbosity >= 2:
                    print "Indexing file " + filename
                indexer.index(filename)
