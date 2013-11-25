"""
Important constants and helpful functions
"""
import glob
import json
import os
from functools import partial

import settings
from settings import LOG as logging
from shared import i18n


kind_slugs = {
    "Video": "v/",
    "Exercise": "e/",
    "Topic": ""
}

topics_file = "topics.json"
map_layout_file = "maplayout_data.json"


# Globals that can be filled
TOPICS          = None
def get_topic_tree(force=False):
    global TOPICS, topics_file
    if TOPICS is None or force:
        TOPICS = json.loads(open(os.path.join(settings.DATA_PATH, topics_file)).read())
        validate_ancestor_ids(TOPICS)  # make sure ancestor_ids are set properly
    return TOPICS


NODE_CACHE = None
def get_node_cache(node_type=None, force=False):
    global NODE_CACHE
    if NODE_CACHE is None or force:
        NODE_CACHE = generate_node_cache(get_topic_tree(force))
    if node_type is None:
        return NODE_CACHE
    else:
        return NODE_CACHE[node_type]


KNOWLEDGEMAP_TOPICS = None
def get_knowledgemap_topics(force=False):
    global KNOWLEDGEMAP_TOPICS, map_layout_file
    if KNOWLEDGEMAP_TOPICS is None or force:
        kmap = json.loads(open(os.path.join(settings.DATA_PATH, map_layout_file)).read())
        KNOWLEDGEMAP_TOPICS = sorted(kmap["topics"].values(), key=lambda k: (k["y"], k["x"]))
    return KNOWLEDGEMAP_TOPICS


SLUG2ID_MAP = None
def get_slug2id_map(force=False):
    global SLUG2ID_MAP
    if SLUG2ID_MAP is None or force:
        SLUG2ID_MAP = generate_slug_to_video_id_map(get_node_cache(force=force))
    return SLUG2ID_MAP


FLAT_TOPIC_TREE = None
def get_flat_topic_tree(force=False):
    global FLAT_TOPIC_TREE
    if FLAT_TOPIC_TREE is None or force:
        FLAT_TOPIC_TREE = generate_flat_topic_tree(get_node_cache(force=force))
    return FLAT_TOPIC_TREE


def validate_ancestor_ids(topictree=None):
    """
    Given the KA Lite topic tree, make sure all parent_id and ancestor_ids are stamped
    """

    if not topictree:
        topictree = get_topic_tree()

    def recurse_nodes(node, ancestor_ids=[]):
        # Add ancestor properties
        if not "parent_id" in node:
            node["parent_id"] = ancestor_ids[-1] if ancestor_ids else None
        if not "ancestor_ids" in node:
            node["ancestor_ids"] = ancestor_ids

        # Do the recursion
        for child in node.get("children", []):
            recurse_nodes(child, ancestor_ids=ancestor_ids + [node["id"]])
    recurse_nodes(topictree)

    return topictree


def generate_slug_to_video_id_map(node_cache=None):
    """
    Go through all videos, and make a map of slug to video_id, for fast look-up later
    """

    node_cache = node_cache or get_node_cache()

    slug2id_map = dict()

    # Make a map from youtube ID to video slug
    for video_id, v in node_cache['Video'].iteritems():
        assert v[0]["slug"] not in slug2id_map, "Make sure there's a 1-to-1 mapping between slug and video_id"
        slug2id_map[v[0]['slug']] = video_id

    return slug2id_map


def generate_flat_topic_tree(node_cache=None):
    categories = node_cache or get_node_cache()
    result = dict()
    # make sure that we only get the slug of child of a topic
    # to avoid redundancy
    for category_name, category in categories.iteritems():
        result[category_name] = {}
        for node_name, node_list in category.iteritems():
            node = node_list[0]
            relevant_data = {
                'title': node['title'],
                'path': node['path'],
                'kind': node['kind'],
                'available': node.get('on_disk', True) or bool(settings.BACKUP_VIDEO_SOURCE),
            }
            result[category_name][node_name] = relevant_data
    return result


def generate_node_cache(topictree=None):#, output_dir=settings.DATA_PATH):
    """
    Given the KA Lite topic tree, generate a dictionary of all Topic, Exercise, and Video nodes.
    """

    if not topictree:
        topictree = get_topic_tree()
    node_cache = {}


    def recurse_nodes(node):
        # Add the node to the node cache
        kind = node["kind"]
        node_cache[kind] = node_cache.get(kind, {})

        if node["id"] not in node_cache[kind]:
            node_cache[kind][node["id"]] = []
        node_cache[kind][node["id"]] += [node]        # Append

        # Do the recursion
        for child in node.get("children", []):
            recurse_nodes(child)
    recurse_nodes(topictree)

    return node_cache


def get_videos(topic):
    """Given a topic node, returns all video node children (non-recursively)"""
    return filter(lambda node: node["kind"] == "Video", topic["children"])


def get_exercises(topic):
    """Given a topic node, returns all exercise node children (non-recursively)"""
    return filter(lambda node: node["kind"] == "Exercise" and node["live"], topic["children"])


def get_live_topics(topic):
    """Given a topic node, returns all children that are not hidden and contain at least one video (non-recursively)"""
    return filter(lambda node: node["kind"] == "Topic" and not node["hide"] and "Video" in node["contains"], topic["children"])


def get_downloaded_youtube_ids(videos_path=settings.CONTENT_ROOT, format="mp4"):
    return [path.split("/")[-1].split(".")[0] for path in glob.glob(os.path.join(videos_path, "*.%s" % format))]


def get_topic_by_path(path, root_node=None):
    """Given a topic path, return the corresponding topic node in the topic hierarchy"""
    # Make sure the root fits
    if not root_node:
        root_node = get_topic_tree()
    if path == root_node["path"]:
        return root_node
    elif not path.startswith(root_node["path"]):
        return {}

    # split into parts (remove trailing slash first)
    parts = path[len(root_node["path"]):-1].split("/")
    cur_node = root_node
    for part in parts:
        cur_node = filter(partial(lambda n, p: n["slug"] == p, p=part), cur_node["children"])
        if cur_node:
            cur_node = cur_node[0]
        else:
            break

    assert not cur_node or cur_node["path"] == path, "Either didn't find it, or found the right thing."

    return cur_node or {}


def get_all_leaves(topic_node=None, leaf_type=None):
    """
    Recurses the topic tree to return all leaves of type leaf_type, at all levels of the tree.

    If leaf_type is None, returns all child nodes of all types and levels.
    """
    if not topic_node:
        topic_node = get_topic_tree()
    leaves = []

    # base case
    if not "children" in topic_node:
        if leaf_type is None or topic_node['kind'] == leaf_type:
            leaves.append(topic_node)

    elif not leaf_type or leaf_type in topic_node["contains"]:
        for child in topic_node["children"]:
            leaves += get_all_leaves(topic_node=child, leaf_type=leaf_type)

    return leaves


def get_topic_leaves(topic_id=None, path=None, leaf_type=None):
    """Given a topic (identified by topic_id or path), return all descendant exercises"""
    assert (topic_id or path) and not (topic_id and path), "Specify topic_id or path, not both."

    if not path:
        topic_node = get_node_cache('Topic').get(topic_id, None)
        if not topic_node:
            return []
        else:
            path = topic_node[0]['path']

    topic_node = get_topic_by_path(path)
    exercises = get_all_leaves(topic_node=topic_node, leaf_type=leaf_type)

    return exercises


def get_topic_exercises(*args, **kwargs):
    """Get all exercises for a particular set of topics"""
    kwargs["leaf_type"] = "Exercise"
    return get_topic_leaves(*args, **kwargs)


def get_topic_videos(*args, **kwargs):
    """Get all videos for a particular set of topics"""
    kwargs["leaf_type"] = "Video"
    return get_topic_leaves(*args, **kwargs)


def get_related_exercises(videos):
    """Given a set of videos, get all of their related exercises."""
    related_exercises = []
    for video in videos:
        if video.get("related_exercise"):
            related_exercises.append(video['related_exercise'])
    return related_exercises


def get_exercise_paths():
    """This function retrieves all the exercise paths.
    """
    exercises = get_node_cache("Exercise").values()
    return [n["path"] for exercise in exercises for n in exercise]


def get_related_videos(exercises, topics=None, possible_videos=None):
    """Given a set of exercises, get all of the videos that say they're related.

    possible_videos: list of videos to consider.
    topics: if not possible_videos, then get the possible videos from a list of topics.
    """
    related_videos = []

    if not possible_videos:
        possible_videos = []
        for topic in (topics or get_node_cache('Topic').values()):
            possible_videos += get_topic_videos(topic_id=topic[0]['id'])

    # Get exercises from videos
    exercise_ids = [ex["id"] for ex in exercises]
    for video in possible_videos:
        if "related_exercise" in video and video["related_exercise"]['id'] in exercise_ids:
            related_videos.append(video)
    return related_videos


def get_video_by_youtube_id(youtube_id):
    # TODO(bcipolli): will need to change for dubbed videos
    video_id = i18n.get_video_id(youtube_id=youtube_id)
    return get_node_cache("Video").get(video_id, [None])[0]


def is_sibling(node1, node2):
    """
    """
    parse_path = lambda n: n["path"] if not kind_slugs[n["kind"]] else n["path"].split("/" + kind_slugs[n["kind"]])[0]

    parent_path1 = parse_path(node1)
    parent_path2 = parse_path(node2)

    return parent_path1 == parent_path2


def delete_parents(node, recurse=True):
    if isinstance(node, (list, tuple)):
        for n in node:
            delete_parents(n, recurse=recurse)
    if "parent" in node:
        del node["parent"]
    if "parents" in node:
        del node["parents"]
    if recurse and "children" in node:
        for child in node["children"]:
            delete_parents(child, recurse=recurse)

    return node
