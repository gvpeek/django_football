# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table(u'people_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('universe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='player_universe', to=orm['core.Universe'])),
            ('signed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('age', self.gf('django.db.models.fields.IntegerField')(default=11)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('constitution', self.gf('django.db.models.fields.IntegerField')()),
            ('retired', self.gf('django.db.models.fields.BooleanField')()),
            ('apex_age', self.gf('django.db.models.fields.IntegerField')()),
            ('growth_rate', self.gf('django.db.models.fields.IntegerField')()),
            ('declination_rate', self.gf('django.db.models.fields.IntegerField')()),
            ('ratings', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('people', ['Player'])

        # Adding model 'Coach'
        db.create_table(u'people_coach', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('universe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coach_universe', to=orm['core.Universe'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('skill', self.gf('django.db.models.fields.IntegerField')()),
            ('play_probabilities', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('fg_dist_probabilities', self.gf('django.db.models.fields.CharField')(max_length=10000)),
        ))
        db.send_create_signal('people', ['Coach'])


    def backwards(self, orm):
        # Deleting model 'Player'
        db.delete_table(u'people_player')

        # Deleting model 'Coach'
        db.delete_table(u'people_coach')


    models = {
        'core.universe': {
            'Meta': {'object_name': 'Universe'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'people.coach': {
            'Meta': {'object_name': 'Coach'},
            'fg_dist_probabilities': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'play_probabilities': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'skill': ('django.db.models.fields.IntegerField', [], {}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coach_universe'", 'to': "orm['core.Universe']"})
        },
        'people.player': {
            'Meta': {'object_name': 'Player'},
            'age': ('django.db.models.fields.IntegerField', [], {'default': '11'}),
            'apex_age': ('django.db.models.fields.IntegerField', [], {}),
            'constitution': ('django.db.models.fields.IntegerField', [], {}),
            'declination_rate': ('django.db.models.fields.IntegerField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'growth_rate': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'ratings': ('django.db.models.fields.IntegerField', [], {}),
            'retired': ('django.db.models.fields.BooleanField', [], {}),
            'signed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player_universe'", 'to': "orm['core.Universe']"})
        }
    }

    complete_apps = ['people']