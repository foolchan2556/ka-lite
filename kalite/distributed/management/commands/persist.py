from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import json
from sqlitedict import SqliteDict

logging = settings.LOG
EXERCISES_FILEPATH = os.path.join(settings.CHANNEL_DATA_PATH, "exercises.json")
EXERCISES_SQLITEPATH = os.path.join(
    settings.CHANNEL_DATA_PATH, "exercises.sqlite")
CONTENT_FILEPATH = os.path.join(settings.CHANNEL_DATA_PATH, "contents.json")
CONTENT_SQLITEPATH = os.path.join(
    settings.CHANNEL_DATA_PATH, "contents.sqlite")


class Command(BaseCommand):

    def handle(self, *args, **options):
        logging.info("Converting...")
        self.convert(EXERCISES_FILEPATH, EXERCISES_SQLITEPATH)
        self.convert(CONTENT_FILEPATH, CONTENT_SQLITEPATH)

    def convert(self, jsonurl, sqliteurl):
        try:
            jsonfile = open(jsonurl)
            items = json.load(jsonfile)
            kalitedict = SqliteDict(sqliteurl)
        except IOError as e:
            logging.error(e)
            return
        for item in items:
            kalitedict[item] = items[item]
        kalitedict.commit()
        kalitedict.close()
        logging.info(jsonurl + " has been converted to " + sqliteurl)
