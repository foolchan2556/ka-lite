from django.core.management.base import BaseCommand, CommandError
import os
import json
from sqlitedict import SqliteDict


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Converting...")
        self.convert('data/khan/contents.json', 'data/khan/contents.sqlite')
        print("Content completed!")
        self.convert('data/khan/exercises.json', 'data/khan/exercises.sqlite')
        print("Exercise completed!")

    def convert(self, jsonurl, sqliteurl):
        url = os.path.join(os.environ['KALITE_DIR'], jsonurl)
        jsonfile = open(url)
        items = json.load(jsonfile)

        kalitedict = SqliteDict(
            os.path.join(os.environ['KALITE_DIR'], sqliteurl))
        for item in items:
            kalitedict[item] = items[item]
        kalitedict.commit()
        kalitedict.close()
