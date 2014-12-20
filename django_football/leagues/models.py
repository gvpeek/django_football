from django.db import models

from core.models import Universe, Year
from teams.models import Team

class League(models.Model):
    def __unicode__(self):
        return self.name
        
    LEVELS = (
        ('pro', 'Pro'),
        ('semipro', 'Semi-Pro'),
        ('amateur', 'Amateur'),
    )
    
    universe = models.ForeignKey(Universe, related_name='league_universe')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=7,choices=LEVELS, default='pro')
    number_playoff_teams = models.IntegerField(default=1)
    
class LeagueMembership(models.Model):
    def __unicode__(self):
        return unicode(self.league) + ' ' + unicode(self.year)
        
    universe = models.ForeignKey(Universe, related_name='membership_universe')
    year = models.ForeignKey(Year, related_name='membership_year')
    league = models.ForeignKey(League, related_name='membership_league')
    team = models.ForeignKey(Team, related_name='membership_team')
    conference = models.IntegerField()
    division = models.IntegerField()
