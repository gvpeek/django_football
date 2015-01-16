# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Universe.new_players_per_year'
        db.add_column(u'core_universe', 'new_players_per_year',
                      self.gf('django.db.models.fields.IntegerField')(default=500),
                      keep_default=False)

        # Adding field 'Universe.new_player_delta_per_year'
        db.add_column(u'core_universe', 'new_player_delta_per_year',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Universe.new_players_per_year'
        db.delete_column(u'core_universe', 'new_players_per_year')

        # Deleting field 'Universe.new_player_delta_per_year'
        db.delete_column(u'core_universe', 'new_player_delta_per_year')


    models = {
        'core.universe': {
            'Meta': {'object_name': 'Universe'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'new_player_delta_per_year': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_players_per_year': ('django.db.models.fields.IntegerField', [], {'default': '500'})
        },
        'core.year': {
            'Meta': {'unique_together': "(('year', 'universe'),)", 'object_name': 'Year'},
            'current_year': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'year_universe'", 'to': "orm['core.Universe']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '1960'})
        }
    }

    complete_apps = ['core']