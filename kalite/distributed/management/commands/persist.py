from django.core.management.base import BaseCommand, CommandError
import os
import json
from sqlitedict import SqliteDict


class Command(BaseCommand):

    def handle(self, *args, **options):
        jsonurl = 'data/khan/contents.json'
        osurl = os.path.join(os.environ['KALITE_DIR'], jsonurl)
        jsonfile = open(osurl)
        items = json.load(jsonfile)

        kalitedict = SqliteDict(os.path.join(os.environ['KALITE_DIR'], 'content_dict.sqlite'))
        for item in items:
            kalitedict[item] = items[item]
        kalitedict.commit()
        for a in kalitedict:
            print(kalitedict[a])
            break