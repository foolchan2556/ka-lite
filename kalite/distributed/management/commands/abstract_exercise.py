from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import json

logging = settings.LOG
EXERCISES_FILEPATH = os.path.join(settings.CHANNEL_DATA_PATH, "exercises.json")
EXERCISES_FILEPATH_BRIEF = os.path.join(
    settings.CHANNEL_DATA_PATH, "exercises_brief.json")


class Command(BaseCommand):

    def handle(self, *args, **options):
        logging.info("Abstracting...")
        self.convert(EXERCISES_FILEPATH, EXERCISES_FILEPATH_BRIEF)

    def convert(self, jsonurl, jsonurl_brief):
        try:
            jsonfile = open(jsonurl)
            items = json.load(jsonfile)
            jsonfile_brief = open(jsonurl_brief, 'w')
        except IOError as e:
            logging.error(e)
            return

        outputitem = {}
        for item in items:
            thisitem = items[item]
            for entry in thisitem:
                if entry == "all_assessment_items" or entry == "uses_assessment_items":
                    outputitem[item] = {}
                    outputitem[item][entry] = thisitem[entry]

        try:
            json.dump(outputitem, jsonfile_brief)
            jsonfile_brief.close()
            logging.info(jsonurl + " has been converted to " + jsonurl_brief)
        except IOError as e:
            logging.error(e)
            return
