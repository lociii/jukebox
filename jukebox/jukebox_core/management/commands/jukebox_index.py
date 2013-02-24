# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand
from optparse import make_option
import os
from jukebox.jukebox_core.models import Artist, Album, Song, Genre
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import ID3NoHeaderError


class FileIndexer:
    def index(self, filename):
        # skip already indexed
        data = Song.objects.filter(Filename__exact=filename)
        if data:
            return

        try:
            id3 = EasyID3(filename)
            tags = {
                "artist": None,
                "title": None,
                "album": None,
                "genre": None,
                "date": None,
                "length": None,
            }

            for k, v in id3.items():
                tags[k] = v[0].lower()

            if tags["artist"] is None or tags["title"] is None:
                print "Artist or title not set in " + \
                    filename + " - skipping file"
                return

            if tags["artist"] is not None:
                tags["artist"], created = Artist.objects.get_or_create(
                    Name=tags["artist"]
                )
            if tags["album"] is not None and tags["artist"] is not None:
                tags["album"], created = Album.objects.get_or_create(
                    Artist=tags["artist"],
                    Title=tags["album"]
                )
            if tags["genre"] is not None:
                tags["genre"], created = Genre.objects.get_or_create(
                    Name=tags["genre"]
                )
            if tags["date"] is not None:
                try:
                    tags["date"] = int(tags["date"])
                except ValueError:
                    tags["date"] = None

            audio = MP3(filename)
            tags["length"] = int(audio.info.length)

            song = Song(
                Artist=tags["artist"],
                Album=tags["album"],
                Genre=tags["genre"],
                Title=tags["title"],
                Year=tags["date"],
                Length=tags["length"],
                Filename=filename
            )
            song.save()
        except HeaderNotFoundError:
            print "File contains invalid header data: " + filename
        except ID3NoHeaderError:
            print "File does not contain an id3 header: " + filename

    def isIndexed(self, filename):
        data = Song.objects.filter(Filename__exact=filename)
        if not data:
            return False
        return True


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--path",
            action="store",
            dest="path",
            help="Music library path to scan"
        ),
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
        self.index(options["path"])

    def index(self, path):
        if not path.endswith("/"):
            path += "/"

        indexer = FileIndexer()

        listing = os.listdir(path)
        for filename in listing:
            filename = path + filename
            if os.path.isdir(filename):
                self.index(filename + "/")
            elif filename.endswith(".mp3"):
                indexer.index(filename)
