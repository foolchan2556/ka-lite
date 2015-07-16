# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AssessmentItem'
        db.create_table(u'topic_tools_assessmentitem', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('item_data', self.gf('django.db.models.fields.TextField')()),
            ('author_names', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'topic_tools', ['AssessmentItem'])

        # Adding model 'Node'
        db.create_table(u'topic_tools_node', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['topic_tools.Node'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sort_order', self.gf('django.db.models.fields.FloatField')(max_length=50)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'topic_tools', ['Node'])

        # Adding model 'ContentNode'
        db.create_table(u'topic_tools_contentnode', (
            (u'node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['topic_tools.Node'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'topic_tools', ['ContentNode'])

        # Adding model 'ContentVideoNode'
        db.create_table(u'topic_tools_contentvideonode', (
            (u'contentnode_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['topic_tools.ContentNode'], unique=True, primary_key=True)),
            ('download_url', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('kind', self.gf('django.db.models.fields.CharField')(default='Video', max_length=20)),
            ('path', self.gf('django.db.models.fields.TextField')()),
            ('format', self.gf('django.db.models.fields.CharField')(default='mp4', max_length=5)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('video_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'topic_tools', ['ContentVideoNode'])


    def backwards(self, orm):
        # Deleting model 'AssessmentItem'
        db.delete_table(u'topic_tools_assessmentitem')

        # Deleting model 'Node'
        db.delete_table(u'topic_tools_node')

        # Deleting model 'ContentNode'
        db.delete_table(u'topic_tools_contentnode')

        # Deleting model 'ContentVideoNode'
        db.delete_table(u'topic_tools_contentvideonode')


    models = {
        u'topic_tools.assessmentitem': {
            'Meta': {'object_name': 'AssessmentItem'},
            'author_names': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'item_data': ('django.db.models.fields.TextField', [], {})
        },
        u'topic_tools.contentnode': {
            'Meta': {'object_name': 'ContentNode', '_ormbases': [u'topic_tools.Node']},
            u'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['topic_tools.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'topic_tools.contentvideonode': {
            'Meta': {'object_name': 'ContentVideoNode', '_ormbases': [u'topic_tools.ContentNode']},
            u'contentnode_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['topic_tools.ContentNode']", 'unique': 'True', 'primary_key': 'True'}),
            'download_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'format': ('django.db.models.fields.CharField', [], {'default': "'mp4'", 'max_length': '5'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': "'Video'", 'max_length': '20'}),
            'path': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'video_id': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'topic_tools.node': {
            'Meta': {'object_name': 'Node'},
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['topic_tools.Node']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {'max_length': '50'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['topic_tools']