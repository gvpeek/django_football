from django.contrib import admin

from teams.models import Team, City, Nickname, Roster, Playbook

class TeamAdmin(admin.ModelAdmin):
    list_display = ('city', 'nickname', 'human_control', 'home_field_advantage', 'coach', 'draft_position_order', 'universe')
    
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'pro', 'semipro', 'amateur', 'region', 'division')

class NicknameAdmin(admin.ModelAdmin):
    list_display = ('name', 'pro', 'semipro',)
    
class RosterAdmin(admin.ModelAdmin):
    list_display = ('year', 'team', 
                    'qb', 'qb_age', 'qb_rating', 
                    'rb', 'rb_age', 'rb_rating', 
                    'wr', 'wr_age', 'wr_rating', 
                    'og', 'og_age', 'og_rating', 
                    'c', 'c_age', 'c_rating', 
                    'ot', 'ot_age', 'ot_rating', 
                    'dt', 'dt_age', 'dt_rating', 
                    'de', 'de_age', 'de_rating', 
                    'lb', 'lb_age', 'lb_rating', 
                    'cb', 'cb_age', 'cb_rating', 
                    's', 's_age', 's_rating', 
                    'k', 'k_age', 'k_rating', 
                    'p', 'p_age', 'p_rating', 
                    'universe')
    list_filter = ('universe',)

class PlaybookAdmin(admin.ModelAdmin):
    list_display = ('name', 'plays')
                    
admin.site.register(Team, TeamAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Nickname, NicknameAdmin)
admin.site.register(Roster, RosterAdmin)
admin.site.register(Playbook, PlaybookAdmin)