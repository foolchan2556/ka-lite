""" abstract_exercise
    This module is used to convert exercises.json file into index for reducing memory usage.
    Usage: kalite manage abstract_exercise
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import json

logging = settings.LOG
EXERCISES_FILEPATH = os.path.join(settings.CHANNEL_DATA_PATH, "exercises.json")
EXERCISES_FILEPATH_BRIEF = os.path.join(
    settings.CHANNEL_DATA_PATH, "exercises_index.json")


class Command(BaseCommand):

    def handle(self, *args, **options):
        logging.info("Abstracting...")
        self.convert(EXERCISES_FILEPATH, EXERCISES_FILEPATH_BRIEF)

    def convert(self, jsonurl, jsonurl_index):
        try:
            jsonfile = open(jsonurl)
            items = json.load(jsonfile)
            jsonfile_index = open(jsonurl_index, 'w')
        except IOError as e:
            logging.error(e)
            return

        outputitem = {}
        for item in items:
            outputitem[item] = None
        try:
            json.dump(outputitem, jsonfile_index)
            jsonfile_index.close()
            logging.info(jsonurl + " has been converted to " + jsonurl_index)
        except IOError as e:
            logging.error(e)
            return
