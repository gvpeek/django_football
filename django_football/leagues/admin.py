from django.contrib import admin

from .models import League, LeagueMembership, Game, Schedule, PlayoffTeams, Champions

class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'number_playoff_teams', 'universe')

class LeagueMembershipAdmin(admin.ModelAdmin):
    list_display = ('league', 'year', 'conference', 'division', 'team', 'universe')
    
class PlayoffTeamsAdmin(admin.ModelAdmin):
    list_display = ('universe', 'year', 'league', 'team', 'seed', 'qualification', 'eliminated')

class ChampionsAdmin(admin.ModelAdmin):
    list_display = ('universe', 'year', 'league', 'team')
    
class GameAdmin(admin.ModelAdmin):
    list_display = ('away_team', 'home_team', 'year', 'universe') 

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('week', 'game_number', 'game', 'played', 'playoff_game', 'year', 'league', 'universe')
    
admin.site.register(League, LeagueAdmin)
admin.site.register(LeagueMembership, LeagueMembershipAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(PlayoffTeams, PlayoffTeamsAdmin)
admin.site.register(Champions, ChampionsAdmin)
