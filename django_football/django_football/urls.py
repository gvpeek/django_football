from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

import core.views
import leagues.views
import teams.views
import stats.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', core.views.index, name='index'),
    url(r'universe/create/$', core.views.universe_create, name='universe_create'),
    url(r'universe/detail/(?P<universe_id>\d+)/$', core.views.show_leagues, name='show_leagues'),
    
    url(r'league/(?P<league_id>\d+)/$', leagues.views.show_league_detail, name='show_league_detail'),
    url(r'league/standings/(?P<league_id>\d+)/$', leagues.views.show_standings, name='show_league_standings'),
    url(r'league/standings/(?P<league_id>\d+)/(?P<year>\d+)/$', leagues.views.show_standings, name='show_league_standings_year'),
    url(r'league/play_game/(?P<game_id>\d+)/$', leagues.views.play_league_game, name='play_league_game'),
    url(r'league/play_week/(?P<league_id>\d+)/(?P<week>\d+)/$', leagues.views.play_league_week, name='play_league_week'),
    url(r'league/play_remaining/(?P<league_id>\d+)/$', leagues.views.play_league_remaining, name='play_league_remaining'),
    
    url(r'team/detail/(?P<team_id>\d+)/(?P<year>\d+)/$', teams.views.show_team_detail, name='show_team_detail'),
    
    url(r'stats/game/(?P<game_id>\d+)/$', stats.views.game_stats, name='show_game_stats'),
    

    # Examples:
    # url(r'^$', 'django_football.views.home', name='home'),
    # url(r'^django_football/', include('django_football.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
