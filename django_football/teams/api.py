from tastypie import fields
from tastypie.resources import ModelResource

from .models import Team, City
        
class CityResource(ModelResource):
    class Meta:
        queryset = City.objects.all()
        resource_name = 'city'

class TeamResource(ModelResource):
    city = fields.ForeignKey(CityResource, 'city', full=True)
    
    class Meta:
        queryset = Team.objects.all()
        resource_name = 'team'