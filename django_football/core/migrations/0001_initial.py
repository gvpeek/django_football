# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Universe'
        db.create_table(u'core_universe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('core', ['Universe'])

        # Adding model 'Year'
        db.create_table(u'core_year', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=1960)),
            ('universe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='year_universe', to=orm['core.Universe'])),
            ('current_year', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'core', ['Year'])

        # Adding unique constraint on 'Year', fields ['year', 'universe']
        db.create_unique(u'core_year', ['year', 'universe_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Year', fields ['year', 'universe']
        db.delete_unique(u'core_year', ['year', 'universe_id'])

        # Deleting model 'Universe'
        db.delete_table(u'core_universe')

        # Deleting model 'Year'
        db.delete_table(u'core_year')


    models = {
        'core.universe': {
            'Meta': {'object_name': 'Universe'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'core.year': {
            'Meta': {'unique_together': "(('year', 'universe'),)", 'object_name': 'Year'},
            'current_year': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'year_universe'", 'to': "orm['core.Universe']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '1960'})
        }
    }

    complete_apps = ['core']