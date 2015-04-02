from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from .models import Champions, League
from core.api import UniverseResource, YearResource
from teams.api import TeamResource

class LeagueResource(ModelResource):
    universe = fields.ForeignKey(UniverseResource, 'universe')
    
    class Meta:
        queryset = League.objects.all()
        resource_name = 'league'

class ChampionsResource(ModelResource):
    universe = fields.ForeignKey(UniverseResource, 'universe')
    year = fields.ForeignKey(YearResource, 'year', full=True)
    league = fields.ForeignKey(LeagueResource, 'league')
    team = fields.ForeignKey(TeamResource, 'team', full=True)
    
    class Meta:
        queryset = Champions.objects.all()
        resource_name = 'champions'
        filtering = { 'team' : ALL_WITH_RELATIONS }