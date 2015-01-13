# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Schedule.playoff_game'
        db.add_column(u'leagues_schedule', 'playoff_game',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Schedule.playoff_game'
        db.delete_column(u'leagues_schedule', 'playoff_game')


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
        u'leagues.champions': {
            'Meta': {'object_name': 'Champions'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'champions_league'", 'to': u"orm['leagues.League']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'champions_team'", 'to': u"orm['teams.Team']"}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'champions_universe'", 'to': "orm['core.Universe']"}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'champions_year'", 'to': "orm['core.Year']"})
        },
        u'leagues.game': {
            'Meta': {'object_name': 'Game'},
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_away_team'", 'to': u"orm['teams.Team']"}),
            'conference_game': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'division_game': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_home_team'", 'to': u"orm['teams.Team']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league_game': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_of_overtime_periods': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'number_of_periods': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'playoff_game': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_universe'", 'to': "orm['core.Universe']"}),
            'use_overtime': ('django.db.models.fields.BooleanField', [], {}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_year'", 'to': "orm['core.Year']"})
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
        u'leagues.playoffteams': {
            'Meta': {'object_name': 'PlayoffTeams'},
            'eliminated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'playoff_league'", 'to': u"orm['leagues.League']"}),
            'qualification': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'seed': ('django.db.models.fields.IntegerField', [], {}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'playoff_team'", 'to': u"orm['teams.Team']"}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'playoff_universe'", 'to': "orm['core.Universe']"}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'playoff_year'", 'to': "orm['core.Year']"})
        },
        u'leagues.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedule_game'", 'to': u"orm['leagues.Game']"}),
            'game_number': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedule_league'", 'to': u"orm['leagues.League']"}),
            'played': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'playoff_game': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedule_universe'", 'to': "orm['core.Universe']"}),
            'week': ('django.db.models.fields.IntegerField', [], {}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'schedule_year'", 'to': "orm['core.Year']"})
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
        u'teams.city': {
            'Meta': {'object_name': 'City'},
            'amateur': ('django.db.models.fields.BooleanField', [], {}),
            'division': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'pro': ('django.db.models.fields.BooleanField', [], {}),
            'region': ('django.db.models.fields.IntegerField', [], {}),
            'semipro': ('django.db.models.fields.BooleanField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'teams.playbook': {
            'Meta': {'object_name': 'Playbook'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'plays': ('django.db.models.fields.CharField', [], {'max_length': '10000'})
        },
        u'teams.team': {
            'Meta': {'object_name': 'Team'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_city'", 'to': u"orm['teams.City']"}),
            'coach': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_coach'", 'to': "orm['people.Coach']"}),
            'draft_position_order': ('django.db.models.fields.CharField', [], {'default': '\'["S", "P", "DT", "LB", "WR", "CB", "OG", "QB", "C", "K", "DE", "OT", "RB"]\'', 'max_length': '200'}),
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