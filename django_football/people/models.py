from django.db import models

from core.models import Universe

class Player(models.Model):
    
    def __unicode__(self):
        return self.last_name + ', ' + self.first_name
        
    POSITIONS = (
        ('QB', 'Quarterback'),
        ('RB', 'Running Back'),
        ('WR', 'Wide Receiver'),
        ('OT', 'Offensive Tackle'),
        ('OG', 'Offensive Guard'),
        ('C', 'Center'),
        ('DT', 'Defensive Tackle'),
        ('DE', 'Defensive End'),
        ('LB', 'Linebacker'),
        ('CB', 'Corner Back'),
        ('S', 'Safety'),
        ('K', 'Kicker'),
        ('P', 'Punter'),
    )
    
    universe = models.ForeignKey(Universe, related_name='player_universe')
    signed = models.BooleanField(default=False)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    age = models.IntegerField(default=11)
    position = models.CharField(max_length=2, choices=POSITIONS)
    constitution = models.IntegerField()
    retired = models.BooleanField()
    apex_age = models.IntegerField()
    growth_rate = models.IntegerField()
    declination_rate = models.IntegerField()
    ratings = models.IntegerField() # need to convert to dict
    future_ratings = models.IntegerField() # need to convert to dict

    class Meta:
        app_label = 'people'

class Coach(models.Model):
    def __unicode__(self):
        return self.last_name + ', ' + self.first_name
    
    universe = models.ForeignKey(Universe, related_name='coach_universe')
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    skill = models.IntegerField()
    play_probabilities = models.CharField(max_length=10000)
    fg_dist_probabilities = models.CharField(max_length=10000)
    
    class Meta:
        app_label = 'people'
