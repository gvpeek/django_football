from django.contrib import admin

from people.models import Player, Coach

def make_free_agent(modeladmin, request, queryset):
    queryset.update(signed=False)
make_free_agent.short_description = "Make selected players free agents"

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'ratings', 'age', 'signed', 'retired', 'universe',)

    actions = [make_free_agent]
    
class CoachAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'skill', 'play_probabilities', 
                    'fg_dist_probabilities') 
                    
admin.site.register(Player, PlayerAdmin)
admin.site.register(Coach, CoachAdmin)