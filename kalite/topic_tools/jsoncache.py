from pylru import lrucache
from django.conf import settings
import os
from sqlitedict import SqliteDict

logging = settings.LOG


class jsoncache():
    size = 0
    cache = None
    kalitedict = None
    sqlitepath = None

    def __init__(self, cachesize=10, sqlpath="exercises.sqlite"):
        self.size = cachesize
        self.cache = lrucache(self.size)
        self.sqlitepath = os.path.join(
            settings.CHANNEL_DATA_PATH, sqlpath)
        self.kalitedict = SqliteDict(sqlitepath)
        logging.info("Constructed a lrucache of size " + self.size)

    def get(self, key, default='[]'):
        if key in cache:
            return cache[key]
        else:
            if key in kalitedict:
                result = kalitedict[key]
                cache[key] = result
                return result
            else:
                return default
