from django.contrib import admin

from core.models import Universe, Year

class UniverseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class YearAdmin(admin.ModelAdmin):
    list_display = ('year', 'current_year', 'universe')

admin.site.register(Universe, UniverseAdmin)
admin.site.register(Year, YearAdmin)
