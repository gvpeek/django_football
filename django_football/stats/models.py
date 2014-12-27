from django.db import models

from core.models import Universe, Year
from leagues.models import League, Game
from teams.models import Team

class Stats(models.Model):
    def __unicode__(self):
        return unicode(self.team) + ' ' + unicode(self.year)
            
    universe = models.ForeignKey(Universe,related_name='teamstats_universe')
    year = models.ForeignKey(Year, related_name='teamstats_year')
    team = models.ForeignKey(Team, related_name='teamstats_team')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    pct = models.DecimalField(max_digits=4, decimal_places=3, default=0.00)
    score = models.IntegerField(default=0)
    opp = models.IntegerField(default=0)
    diff = models.IntegerField(default=0)
    score_by_period = models.CommaSeparatedIntegerField(max_length=30, default=[0,0,0,0])
    total_yards = models.IntegerField(default=0)
    pass_att = models.IntegerField(default=0)
    pass_comp = models.IntegerField(default=0)
    completion_pct = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    pass_yards = models.IntegerField(default=0)
    pass_td = models.IntegerField(default=0)
    intercepted = models.IntegerField(default=0)
    sacked = models.IntegerField(default=0)
    rush_att = models.IntegerField(default=0)
    rush_yards = models.IntegerField(default=0)
    rush_td = models.IntegerField(default=0)
    fumbles = models.IntegerField(default=0)
    fg_att = models.IntegerField(default=0)
    fg = models.IntegerField(default=0)
    xp_att = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    conv_att = models.IntegerField(default=0)
    conv = models.IntegerField(default=0)
    punts = models.IntegerField(default=0)
    punt_yards = models.IntegerField(default=0)
    punt_touchbacks = models.IntegerField(default=0)
    punt_blocks = models.IntegerField(default=0)
    punt_returns = models.IntegerField(default=0)
    punt_return_yards = models.IntegerField(default=0)
    kickoffs = models.IntegerField(default=0)
    kickoff_yards = models.IntegerField(default=0)
    kickoff_touchbacks = models.IntegerField(default=0)
    kick_returns = models.IntegerField(default=0)
    kick_return_yards = models.IntegerField(default=0)
    safeties = models.IntegerField(default=0)

class TeamStats(Stats): pass  
class PlayoffTeamStats(Stats): pass

class GameStats(models.Model):
    def __unicode__(self):
        return unicode(self.team) + ' ' + unicode(self.score)
        
    OUTCOMES = (
        ('W', 'Win'),
        ('L', 'Loss'),
        ('T', 'Tie'),
    )
            
    universe = models.ForeignKey(Universe,related_name='gamestats_universe')
    year = models.ForeignKey(Year, related_name='gamestats_year')
    game = models.ForeignKey(Game, related_name='gamestats_game')
    team = models.ForeignKey(Team, related_name='gamestats_team')
    outcome = models.CharField(max_length=1, choices=OUTCOMES)
    score = models.IntegerField(default=0)
    score_by_period = models.CommaSeparatedIntegerField(max_length=30, default=[0,0,0,0])
    total_yards = models.IntegerField(default=0)
    pass_att = models.IntegerField(default=0)
    pass_comp = models.IntegerField(default=0)
    completion_pct = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    pass_yards = models.IntegerField(default=0)
    pass_td = models.IntegerField(default=0)
    intercepted = models.IntegerField(default=0)
    sacked = models.IntegerField(default=0)
    rush_att = models.IntegerField(default=0)
    rush_yards = models.IntegerField(default=0)
    rush_td = models.IntegerField(default=0)
    fumbles = models.IntegerField(default=0)
    fg_att = models.IntegerField(default=0)
    fg = models.IntegerField(default=0)
    xp_att = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    conv_att = models.IntegerField(default=0)
    conv = models.IntegerField(default=0)
    punts = models.IntegerField(default=0)
    punt_yards = models.IntegerField(default=0)
    punt_touchbacks = models.IntegerField(default=0)
    punt_blocks = models.IntegerField(default=0)
    punt_returns = models.IntegerField(default=0)
    punt_return_yards = models.IntegerField(default=0)
    kickoffs = models.IntegerField(default=0)
    kickoff_yards = models.IntegerField(default=0)
    kickoff_touchbacks = models.IntegerField(default=0)
    kick_returns = models.IntegerField(default=0)
    kick_return_yards = models.IntegerField(default=0)
    safeties = models.IntegerField(default=0)
