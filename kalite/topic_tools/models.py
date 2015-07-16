from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class AssessmentItem(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    item_data = models.TextField()  # A serialized JSON blob
    author_names = models.CharField(max_length=200)  # A serialized JSON list

# Topic tree models
#
# To ease migration once content-curation is ready, we should make
# sure to have the same attribute names and types with the models
# found here:
# https://github.com/fle-internal/content-curation/blob/master/contentcuration/contentcuration/models.py

class Node(MPTTModel):

    id = models.CharField(max_length=50, primary_key=True)

    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')

    name = models.CharField(
        max_length=50,
        verbose_name=_("name")
    )

    sort_order = models.FloatField(
        max_length=50,
        verbose_name=_("sort order")
    )


class ContentNode(Node):
    title = models.CharField(
        max_length=50,
        verbose_name=_("title")
    )


class ContentVideoNode(ContentNode):

    download_url = models.CharField(
        max_length=100
    )

    duration = models.IntegerField(

    )

    kind = models.CharField(
        max_length=20,
        default="Video",
    )

    path = models.TextField()

    format = models.CharField(
        max_length=5,
        default="mp4",
    )

    slug = models.CharField(
        max_length=20
    )

    video_id = models.CharField(
        max_length=20
    )
