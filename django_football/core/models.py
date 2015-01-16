from django.db import models

class Universe(models.Model):
    def __unicode__(self):
        return self.name
        
    name = models.CharField(max_length=60)
    new_players_per_year = models.IntegerField(default=500)
    new_player_delta_per_year = models.IntegerField(default=0)

    class Meta:
        app_label = 'core'

class Year(models.Model):
    def __unicode__(self):
        return unicode(self.year)
        
    year = models.IntegerField(default=1960)
    universe = models.ForeignKey(Universe, related_name='year_universe')
    current_year = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('year','universe')
        app_label = 'core'