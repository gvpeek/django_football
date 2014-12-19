import json
from random import shuffle

from django.db import models

from core.models import Universe, Year
from people.models import Coach, Player

class City(models.Model):
    def __unicode__(self):
        return self.name
        
    name = models.CharField(max_length=60)
    state = models.CharField(max_length=2)
    pro = models.BooleanField() 
    semipro = models.BooleanField()
    amateur = models.BooleanField()
    region = models.IntegerField()
    division = models.IntegerField()
    
class Nickname(models.Model):
    def __unicode__(self):
        return self.name
        
    name = models.CharField(max_length=60)
    pro = models.BooleanField()
    semipro = models.BooleanField()  

class Playbook(models.Model):
    def __unicode__(self):
        return self.name
        
    name = models.CharField(max_length=60)
    plays = models.CharField(max_length=10000)

def get_draft_position_order():
    order =['QB','RB','WR','OT','OG','C','DT','DE','LB','CB','S','K','P']
    shuffle(order)
    return json.dumps(order)

class Team(models.Model):
    def __unicode__(self):
        return unicode(self.city) + ' ' +unicode(self.nickname)
    
    universe = models.ForeignKey(Universe, related_name='team_universe')
    city = models.CharField(max_length=60)
    nickname = models.CharField(max_length=60)
    human_control = models.BooleanField(default=False)
    home_field_advantage = models.IntegerField(default=1)
    draft_position_order = models.CharField(max_length=200,
                                     default=get_draft_position_order())
    coach = models.ForeignKey(Coach, related_name='team_coach')
    playbook = models.ForeignKey(Playbook, related_name='team_playbook') 
    primary_color  = models.CommaSeparatedIntegerField(max_length=30)
    secondary_color = models.CommaSeparatedIntegerField(max_length=30)

class Roster(models.Model):
    def __unicode__(self):
        return unicode(self.team) + ' ' + unicode(self.year)
    
    universe = models.ForeignKey(Universe, related_name='roster_universe')    
    team = models.ForeignKey(Team, related_name='roster_team')
    year = models.ForeignKey(Year, related_name='roster_year')
    qb = models.ForeignKey(Player, 
                           related_name='quarterback', 
                           null=True,
                           blank=True,
                           limit_choices_to={'position' : 'QB',
                                             'retired' : False})
    qb_age = models.IntegerField(null=True, blank=True)
    qb_rating = models.IntegerField(null=True, blank=True)
    rb = models.ForeignKey(Player, 
                           related_name='running back', 
                           null=True,
                           blank=True,
                           limit_choices_to={'position' : 'RB',
                                             'retired' : False})
    rb_age = models.IntegerField(null=True, blank=True)
    rb_rating = models.IntegerField(null=True, blank=True)
    wr = models.ForeignKey(Player, 
                           related_name='wide receiver', 
                           null=True,
                           blank=True,
                           limit_choices_to={'position' : 'WR',
                                             'retired' : False})
    wr_age = models.IntegerField(null=True, blank=True)
    wr_rating = models.IntegerField(null=True, blank=True)
    og = models.ForeignKey(Player, 
                           related_name='offensive guard', 
                           null=True,
                           blank=True,
                           limit_choices_to={'position' : 'OG',
                                             'retired' : False})
    og_age = models.IntegerField(null=True, blank=True)
    og_rating = models.IntegerField(null=True, blank=True)
    ot = models.ForeignKey(Player, 
                           related_name='offensive tackle', 
                           null=True,
                           blank=True,
                           limit_choices_to={'position' : 'OT',
                                             'retired' : False})
    ot_age = models.IntegerField(null=True, blank=True)
    ot_rating = models.IntegerField(null=True, blank=True)
    c = models.ForeignKey(Player, 
                           related_name='center', 
                           null=True,
                           blank=True,
                           limit_choices_to={'position' : 'C',
                                             'retired' : False})
    c_age = models.IntegerField(null=True, blank=True)
    c_rating = models.IntegerField(null=True, blank=True)
    de = models.ForeignKey(Player, 
                           related_name='defensive end', 
                           null=True,
                           blank=True,
                           limit_choices_to={'position' : 'DE',
                                             'retired' : False})
    de_age = models.IntegerField(null=True, blank=True)
    de_rating = models.IntegerField(null=True, blank=True)
    dt = models.ForeignKey(Player, 
                           related_name='defensive tackle', 
                           null=True,
                           blank=True,
                           limit_choices_to={'position' : 'DT',
                                             'retired' : False})
    dt_age = models.IntegerField(null=True, blank=True)
    dt_rating = models.IntegerField(null=True, blank=True)
    lb = models.ForeignKey(Player, 
                           related_name='linebacker', 
                           null=True,
                           blank=True,
                           limit_choices_to={'position' : 'LB',
                                             'retired' : False})
    lb_age = models.IntegerField(null=True, blank=True)
    lb_rating = models.IntegerField(null=True, blank=True)
    cb = models.ForeignKey(Player, 
                           related_name='cornerback', 
                           null=True,
                           blank=True,
                           limit_choices_to={'position' : 'CB',
                                             'retired' : False})
    cb_age = models.IntegerField(null=True, blank=True)
    cb_rating = models.IntegerField(null=True, blank=True)
    s = models.ForeignKey(Player, 
                          related_name='safety', 
                          null=True,
                          blank=True,
                          limit_choices_to={'position' : 'S',
                                            'retired' : False})
    s_age = models.IntegerField(null=True, blank=True)
    s_rating = models.IntegerField(null=True, blank=True)
    p = models.ForeignKey(Player, 
                          related_name='punter', 
                          null=True,
                          blank=True,
                          limit_choices_to={'position' : 'P',
                                            'retired' : False})
    p_age = models.IntegerField(null=True, blank=True)
    p_rating = models.IntegerField(null=True, blank=True)
    k = models.ForeignKey(Player, 
                          related_name='kicker', 
                          null=True,
                          blank=True,
                          limit_choices_to={'position' : 'K',
                                            'retired' : False})
    k_age = models.IntegerField(null=True, blank=True)
    k_rating = models.IntegerField(null=True, blank=True)
    
    def get_positions(self):
        return ['qb', 'rb', 'wr', 'og', 'c', 'ot', 'dt', 'de', 'lb', 'cb', 's', 'k', 'p']
