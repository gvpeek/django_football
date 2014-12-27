# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stats'
        db.create_table(u'stats_stats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('universe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='teamstats_universe', to=orm['core.Universe'])),
            ('year', self.gf('django.db.models.fields.related.ForeignKey')(related_name='teamstats_year', to=orm['core.Year'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='teamstats_team', to=orm['teams.Team'])),
            ('wins', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('losses', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ties', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pct', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=4, decimal_places=3)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('opp', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('diff', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('score_by_period', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=[0, 0, 0, 0], max_length=30)),
            ('total_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pass_att', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pass_comp', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('completion_pct', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=3, decimal_places=2)),
            ('pass_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pass_td', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('intercepted', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sacked', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rush_att', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rush_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rush_td', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fumbles', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fg_att', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fg', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('xp_att', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('xp', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('conv_att', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('conv', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('punts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('punt_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('punt_touchbacks', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('punt_blocks', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('punt_returns', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('punt_return_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('kickoffs', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('kickoff_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('kickoff_touchbacks', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('kick_returns', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('kick_return_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('safeties', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'stats', ['Stats'])

        # Adding model 'TeamStats'
        db.create_table(u'stats_teamstats', (
            (u'stats_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['stats.Stats'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'stats', ['TeamStats'])

        # Adding model 'PlayoffTeamStats'
        db.create_table(u'stats_playoffteamstats', (
            (u'stats_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['stats.Stats'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'stats', ['PlayoffTeamStats'])

        # Adding model 'GameStats'
        db.create_table(u'stats_gamestats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('universe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gamestats_universe', to=orm['core.Universe'])),
            ('year', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gamestats_year', to=orm['core.Year'])),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gamestats_game', to=orm['leagues.Game'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gamestats_team', to=orm['teams.Team'])),
            ('outcome', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('score_by_period', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=[0, 0, 0, 0], max_length=30)),
            ('total_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pass_att', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pass_comp', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('completion_pct', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=3, decimal_places=2)),
            ('pass_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pass_td', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('intercepted', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sacked', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rush_att', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rush_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rush_td', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fumbles', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fg_att', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fg', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('xp_att', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('xp', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('conv_att', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('conv', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('punts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('punt_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('punt_touchbacks', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('punt_blocks', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('punt_returns', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('punt_return_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('kickoffs', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('kickoff_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('kickoff_touchbacks', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('kick_returns', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('kick_return_yards', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('safeties', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'stats', ['GameStats'])


    def backwards(self, orm):
        # Deleting model 'Stats'
        db.delete_table(u'stats_stats')

        # Deleting model 'TeamStats'
        db.delete_table(u'stats_teamstats')

        # Deleting model 'PlayoffTeamStats'
        db.delete_table(u'stats_playoffteamstats')

        # Deleting model 'GameStats'
        db.delete_table(u'stats_gamestats')


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
        u'stats.gamestats': {
            'Meta': {'object_name': 'GameStats'},
            'completion_pct': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '3', 'decimal_places': '2'}),
            'conv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'conv_att': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fg': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fg_att': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fumbles': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gamestats_game'", 'to': u"orm['leagues.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intercepted': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'kick_return_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'kick_returns': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'kickoff_touchbacks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'kickoff_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'kickoffs': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'outcome': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'pass_att': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pass_comp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pass_td': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pass_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'punt_blocks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'punt_return_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'punt_returns': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'punt_touchbacks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'punt_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'punts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rush_att': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rush_td': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rush_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sacked': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'safeties': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score_by_period': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '[0, 0, 0, 0]', 'max_length': '30'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gamestats_team'", 'to': u"orm['teams.Team']"}),
            'total_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gamestats_universe'", 'to': "orm['core.Universe']"}),
            'xp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'xp_att': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gamestats_year'", 'to': "orm['core.Year']"})
        },
        u'stats.playoffteamstats': {
            'Meta': {'object_name': 'PlayoffTeamStats', '_ormbases': [u'stats.Stats']},
            u'stats_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['stats.Stats']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'stats.stats': {
            'Meta': {'object_name': 'Stats'},
            'completion_pct': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '3', 'decimal_places': '2'}),
            'conv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'conv_att': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'diff': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fg': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fg_att': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fumbles': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intercepted': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'kick_return_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'kick_returns': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'kickoff_touchbacks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'kickoff_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'kickoffs': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'opp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pass_att': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pass_comp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pass_td': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pass_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pct': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '4', 'decimal_places': '3'}),
            'punt_blocks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'punt_return_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'punt_returns': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'punt_touchbacks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'punt_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'punts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rush_att': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rush_td': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rush_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sacked': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'safeties': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score_by_period': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '[0, 0, 0, 0]', 'max_length': '30'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teamstats_team'", 'to': u"orm['teams.Team']"}),
            'ties': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_yards': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teamstats_universe'", 'to': "orm['core.Universe']"}),
            'wins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'xp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'xp_att': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teamstats_year'", 'to': "orm['core.Year']"})
        },
        u'stats.teamstats': {
            'Meta': {'object_name': 'TeamStats', '_ormbases': [u'stats.Stats']},
            u'stats_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['stats.Stats']", 'unique': 'True', 'primary_key': 'True'})
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
            'draft_position_order': ('django.db.models.fields.CharField', [], {'default': '\'["P", "K", "OT", "S", "WR", "CB", "OG", "C", "QB", "DT", "RB", "LB", "DE"]\'', 'max_length': '200'}),
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

    complete_apps = ['stats']