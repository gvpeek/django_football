from tastypie.resources import ModelResource

from .models import Universe, Year

class UniverseResource(ModelResource):
    class Meta:
        queryset = Universe.objects.all()
        resource_name = 'universe'
        
class YearResource(ModelResource):
    class Meta:
        queryset = Year.objects.all()
        resource_name = 'year'