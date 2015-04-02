from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from .models import Team, City
        
class CityResource(ModelResource):
    class Meta:
        queryset = City.objects.all()
        resource_name = 'city'
        filtering = {'name' : ALL}

class TeamResource(ModelResource):
    city = fields.ForeignKey(CityResource, 'city', full=True)
    
    class Meta:
        queryset = Team.objects.all()
        resource_name = 'team'
        excludes = ['primary_color', 'secondary_color']
        filtering = {'nickname' : ALL,
                     'city' : ALL_WITH_RELATIONS}