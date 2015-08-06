from pylru import lrucache
from django.conf import settings
import os
from sqlitedict import SqliteDict

logging = settings.LOG

# Class for the node objects.


class _dlnode(object):

    def __init__(self):
        self.empty = True


class jsoncache(lrucache):

    def __init__(self, cachesize=10, sqlpath="exercises.sqlite"):
        lrucache.__init__(self, size=cachesize)
        self.sqlitepath = os.path.join(
            settings.CHANNEL_DATA_PATH, sqlpath)
        self.kalitedict = SqliteDict(self.sqlitepath, autocommit=True)
        logging.info("Constructed a lrucache of size " + str(cachesize))

    def __getitem__(self, key):
        default = '[]'
        if key in self.table:
            return self.table[key].value
        else:
            if key in self.kalitedict:
                result = self.kalitedict[key]
                self[key] = result
                return result
            else:
                return default

    def __setitem__(self, key, value):
        # First, see if any value is stored under 'key' in the cache already.
        # If so we are going to replace that value with the new one.
        if key in self.table:

            # Lookup the node
            node = self.table[key]

            # Replace the value.
            node.value = value

            # Update the list ordering.
            self.mtf(node)
            self.head = node

            return

        # Ok, no value is currently stored under 'key' in the cache. We need
        # to choose a node to place the new item in. There are two cases. If
        # the cache is full some item will have to be pushed out of the
        # cache. We want to choose the node with the least recently used
        # item. This is the node at the tail of the list. If the cache is not
        # full we want to choose a node that is empty. Because of the way the
        # list is managed, the empty nodes are always together at the tail
        # end of the list. Thus, in either case, by chooseing the node at the
        # tail of the list our conditions are satisfied.

        # Since the list is circular, the tail node directly preceeds the
        # 'head' node.
        node = self.head.prev

        # If the node already contains something we need to remove the old
        # key from the dictionary.
        if not node.empty:
            if self.callback is not None:
                self.callback(node.key, node.value)
            # store the item into sqlite before we remove the key
            self.kalitedict[node.key] = node.value
            del self.table[node.key]

        # Place the new key and value in the node
        node.empty = False
        node.key = key
        node.value = value

        # Add the node to the dictionary under the new key.
        self.table[key] = node

        # We need to move the node to the head of the list. The node is the
        # tail node, so it directly preceeds the head node due to the list
        # being circular. Therefore, the ordering is already correct, we just
        # need to adjust the 'head' variable.
        self.head = node
