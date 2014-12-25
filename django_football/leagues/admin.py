from django.contrib import admin

from .models import League, LeagueMembership

class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'number_playoff_teams', 'universe')

class LeagueMembershipAdmin(admin.ModelAdmin):
    list_display = ('league', 'year', 'conference', 'division', 'team', 'universe')
    
admin.site.register(League, LeagueAdmin)
admin.site.register(LeagueMembership, LeagueMembershipAdmin)
