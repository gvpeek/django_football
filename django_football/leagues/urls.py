from django.conf.urls import patterns, url

import leagues.views

urlpatterns = patterns('',
    url(r'^(?P<league_id>\d+)/$', leagues.views.show_league_detail, name='show_league_detail'),
    url(r'standings/(?P<league_id>\d+)/$', leagues.views.show_standings, name='show_league_standings'),
    url(r'standings/(?P<league_id>\d+)/(?P<year>\d+)/$', leagues.views.show_standings, name='show_league_standings_year'),
    url(r'play_game/(?P<game_id>\d+)/$', leagues.views.play_league_game, name='play_league_game'),
    url(r'play_week/(?P<league_id>\d+)/(?P<week>\d+)/$', leagues.views.play_league_week, name='play_league_week'),
    url(r'play_remaining/(?P<league_id>\d+)/$', leagues.views.play_league_remaining, name='play_league_remaining'),
)