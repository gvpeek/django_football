from django.contrib import admin

from stats.models import TeamStats, GameStats, PlayoffTeamStats

class TeamStatsAdmin(admin.ModelAdmin):
    list_display = ('team', 'year', 'wins', 'losses', 'ties', 'pct', 'score', 
                    'opp', 'diff', 'score_by_period', 'total_yards', 'pass_att',  
                    'pass_comp', 'completion_pct', 'pass_yards', 'pass_td',  
                    'intercepted', 'sacked', 'rush_att', 'rush_yards', 
                    'rush_td', 'fumbles', 'universe')

class PlayoffTeamStatsAdmin(TeamStatsAdmin): pass

class GameStatsAdmin(admin.ModelAdmin):
    list_display = ('team', 'game', 'year', 'outcome', 'score', 'score_by_period', 
                    'total_yards', 'pass_att',  'pass_comp', 'completion_pct', 
                    'pass_yards', 'pass_td',  'intercepted', 'sacked', 'rush_att', 
                    'rush_yards', 'rush_td', 'fumbles', 'universe')
                    
admin.site.register(TeamStats, TeamStatsAdmin)
admin.site.register(GameStats, GameStatsAdmin)
admin.site.register(PlayoffTeamStats, PlayoffTeamStatsAdmin)
