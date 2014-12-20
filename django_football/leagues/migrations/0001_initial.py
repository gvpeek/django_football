# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'League'
        db.create_table(u'leagues_league', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('universe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='league_universe', to=orm['core.Universe'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('level', self.gf('django.db.models.fields.CharField')(default='pro', max_length=7)),
            ('number_playoff_teams', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'leagues', ['League'])

        # Adding model 'LeagueMembership'
        db.create_table(u'leagues_leaguemembership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('universe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='membership_universe', to=orm['core.Universe'])),
            ('year', self.gf('django.db.models.fields.related.ForeignKey')(related_name='membership_year', to=orm['core.Year'])),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(related_name='membership_league', to=orm['leagues.League'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='membership_team', to=orm['teams.Team'])),
            ('conference', self.gf('django.db.models.fields.IntegerField')()),
            ('division', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'leagues', ['LeagueMembership'])


    def backwards(self, orm):
        # Deleting model 'League'
        db.delete_table(u'leagues_league')

        # Deleting model 'LeagueMembership'
        db.delete_table(u'leagues_leaguemembership')


    models = {
        'core.universe': {
            'Meta': {'object_name': 'Universe'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'core.year': {
            'Meta': {'unique_together': "(('year', 'universe'),)", 'object_name': 'Year'},
            'current_year': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'year_universe'", 'to': "orm['core.Universe']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '1960'})
        },
        u'leagues.league': {
            'Meta': {'object_name': 'League'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'default': "'pro'", 'max_length': '7'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number_playoff_teams': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'league_universe'", 'to': "orm['core.Universe']"})
        },
        u'leagues.leaguemembership': {
            'Meta': {'object_name': 'LeagueMembership'},
            'conference': ('django.db.models.fields.IntegerField', [], {}),
            'division': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'membership_league'", 'to': u"orm['leagues.League']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'membership_team'", 'to': u"orm['teams.Team']"}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'membership_universe'", 'to': "orm['core.Universe']"}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'membership_year'", 'to': "orm['core.Year']"})
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
        u'teams.playbook': {
            'Meta': {'object_name': 'Playbook'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'plays': ('django.db.models.fields.CharField', [], {'max_length': '10000'})
        },
        u'teams.team': {
            'Meta': {'object_name': 'Team'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'coach': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_coach'", 'to': "orm['people.Coach']"}),
            'draft_position_order': ('django.db.models.fields.CharField', [], {'default': '\'["C", "RB", "QB", "DT", "OG", "OT", "P", "LB", "CB", "K", "DE", "S", "WR"]\'', 'max_length': '200'}),
            'home_field_advantage': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'human_control': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'playbook': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_playbook'", 'to': u"orm['teams.Playbook']"}),
            'primary_color': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '30'}),
            'secondary_color': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '30'}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_universe'", 'to': "orm['core.Universe']"})
        }
    }

    complete_apps = ['leagues']