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

class Game(models.Model):
    def __unicode__(self):
        return unicode(self.away_team) + ' at ' + unicode(self.home_team)
        
    universe = models.ForeignKey(Universe, related_name='game_universe')
    year = models.ForeignKey(Year, related_name='game_year')
    home_team = models.ForeignKey(Team, related_name='game_home_team')
    away_team = models.ForeignKey(Team, related_name='game_away_team')
    number_of_periods = models.IntegerField(default=4)
    use_overtime = models.BooleanField()
    number_of_overtime_periods = models.IntegerField(default=1)
    league_game = models.BooleanField(default=False)
    division_game = models.BooleanField(default=False)
    conference_game = models.BooleanField(default=False)
    playoff_game = models.BooleanField(default=False)
    
class Schedule(models.Model):
    def __unicode__(self):
        return unicode(self.week) + ' - ' + unicode(self.game_number) + ' ' + unicode(self.game)
    
    universe = models.ForeignKey(Universe, related_name='schedule_universe')
    year = models.ForeignKey(Year, related_name='schedule_year')
    league = models.ForeignKey(League, related_name='schedule_league')
    game = models.ForeignKey(Game, related_name='schedule_game')
    week = models.IntegerField()
    game_number = models.IntegerField()
    playoff_game = models.BooleanField(default=False)
    played = models.BooleanField(default=False)

class PlayoffTeams(models.Model):
    def __unicode__(self):
        return unicode(self.seed) + ' - ' + unicode(self.team) 

    universe = models.ForeignKey(Universe, related_name='playoff_universe')
    year = models.ForeignKey(Year, related_name='playoff_year')
    league = models.ForeignKey(League, related_name='playoff_league')
    team = models.ForeignKey(Team, related_name='playoff_team')
    seed = models.IntegerField()
    qualification = models.CharField(max_length=9)
    eliminated = models.BooleanField(default=False)

class Champions(models.Model):
    def __unicode__(self):
        return unicode(self.team) 

    universe = models.ForeignKey(Universe, related_name='champions_universe')
    year = models.ForeignKey(Year, related_name='champions_year')
    league = models.ForeignKey(League, related_name='champions_league')
    team = models.ForeignKey(Team, related_name='champions_team')