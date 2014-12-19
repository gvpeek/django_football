# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'City'
        db.create_table(u'teams_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('pro', self.gf('django.db.models.fields.BooleanField')()),
            ('semipro', self.gf('django.db.models.fields.BooleanField')()),
            ('amateur', self.gf('django.db.models.fields.BooleanField')()),
            ('region', self.gf('django.db.models.fields.IntegerField')()),
            ('division', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'teams', ['City'])

        # Adding model 'Nickname'
        db.create_table(u'teams_nickname', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('pro', self.gf('django.db.models.fields.BooleanField')()),
            ('semipro', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'teams', ['Nickname'])

        # Adding model 'Playbook'
        db.create_table(u'teams_playbook', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('plays', self.gf('django.db.models.fields.CharField')(max_length=10000)),
        ))
        db.send_create_signal(u'teams', ['Playbook'])

        # Adding model 'Team'
        db.create_table(u'teams_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('universe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_universe', to=orm['core.Universe'])),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('human_control', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('home_field_advantage', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('draft_position_order', self.gf('django.db.models.fields.CharField')(default='["DT", "LB", "C", "P", "OT", "K", "CB", "S", "OG", "RB", "QB", "WR", "DE"]', max_length=200)),
            ('coach', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_coach', to=orm['people.Coach'])),
            ('playbook', self.gf('django.db.models.fields.related.ForeignKey')(related_name='team_playbook', to=orm['teams.Playbook'])),
            ('primary_color', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=30)),
            ('secondary_color', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=30)),
        ))
        db.send_create_signal(u'teams', ['Team'])

        # Adding model 'Roster'
        db.create_table(u'teams_roster', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('universe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='roster_universe', to=orm['core.Universe'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='roster_team', to=orm['teams.Team'])),
            ('year', self.gf('django.db.models.fields.related.ForeignKey')(related_name='roster_year', to=orm['core.Year'])),
            ('qb', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='quarterback', null=True, to=orm['people.Player'])),
            ('qb_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('qb_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rb', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='running back', null=True, to=orm['people.Player'])),
            ('rb_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rb_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('wr', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='wide receiver', null=True, to=orm['people.Player'])),
            ('wr_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('wr_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('og', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='offensive guard', null=True, to=orm['people.Player'])),
            ('og_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('og_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ot', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='offensive tackle', null=True, to=orm['people.Player'])),
            ('ot_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ot_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('c', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='center', null=True, to=orm['people.Player'])),
            ('c_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('c_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('de', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='defensive end', null=True, to=orm['people.Player'])),
            ('de_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('de_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dt', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='defensive tackle', null=True, to=orm['people.Player'])),
            ('dt_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dt_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lb', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='linebacker', null=True, to=orm['people.Player'])),
            ('lb_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lb_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cb', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cornerback', null=True, to=orm['people.Player'])),
            ('cb_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cb_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('s', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='safety', null=True, to=orm['people.Player'])),
            ('s_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('s_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('p', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='punter', null=True, to=orm['people.Player'])),
            ('p_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('p_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('k', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='kicker', null=True, to=orm['people.Player'])),
            ('k_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('k_rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'teams', ['Roster'])


    def backwards(self, orm):
        # Deleting model 'City'
        db.delete_table(u'teams_city')

        # Deleting model 'Nickname'
        db.delete_table(u'teams_nickname')

        # Deleting model 'Playbook'
        db.delete_table(u'teams_playbook')

        # Deleting model 'Team'
        db.delete_table(u'teams_team')

        # Deleting model 'Roster'
        db.delete_table(u'teams_roster')


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
        u'teams.nickname': {
            'Meta': {'object_name': 'Nickname'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'pro': ('django.db.models.fields.BooleanField', [], {}),
            'semipro': ('django.db.models.fields.BooleanField', [], {})
        },
        u'teams.playbook': {
            'Meta': {'object_name': 'Playbook'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'plays': ('django.db.models.fields.CharField', [], {'max_length': '10000'})
        },
        u'teams.roster': {
            'Meta': {'object_name': 'Roster'},
            'c': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'center'", 'null': 'True', 'to': "orm['people.Player']"}),
            'c_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'c_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cb': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cornerback'", 'null': 'True', 'to': "orm['people.Player']"}),
            'cb_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cb_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'de': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'defensive end'", 'null': 'True', 'to': "orm['people.Player']"}),
            'de_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'de_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dt': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'defensive tackle'", 'null': 'True', 'to': "orm['people.Player']"}),
            'dt_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dt_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'k': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'kicker'", 'null': 'True', 'to': "orm['people.Player']"}),
            'k_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'k_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lb': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'linebacker'", 'null': 'True', 'to': "orm['people.Player']"}),
            'lb_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lb_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'og': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'offensive guard'", 'null': 'True', 'to': "orm['people.Player']"}),
            'og_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'og_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ot': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'offensive tackle'", 'null': 'True', 'to': "orm['people.Player']"}),
            'ot_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ot_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'p': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'punter'", 'null': 'True', 'to': "orm['people.Player']"}),
            'p_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'p_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'qb': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quarterback'", 'null': 'True', 'to': "orm['people.Player']"}),
            'qb_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'qb_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rb': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'running back'", 'null': 'True', 'to': "orm['people.Player']"}),
            'rb_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rb_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            's': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'safety'", 'null': 'True', 'to': "orm['people.Player']"}),
            's_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            's_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roster_team'", 'to': u"orm['teams.Team']"}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roster_universe'", 'to': "orm['core.Universe']"}),
            'wr': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'wide receiver'", 'null': 'True', 'to': "orm['people.Player']"}),
            'wr_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wr_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roster_year'", 'to': "orm['core.Year']"})
        },
        u'teams.team': {
            'Meta': {'object_name': 'Team'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'coach': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team_coach'", 'to': "orm['people.Coach']"}),
            'draft_position_order': ('django.db.models.fields.CharField', [], {'default': '\'["DT", "LB", "C", "P", "OT", "K", "CB", "S", "OG", "RB", "QB", "WR", "DE"]\'', 'max_length': '200'}),
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

    complete_apps = ['teams']