from django.conf.urls import patterns, url

import stats.views

urlpatterns = patterns('',
    url(r'game/(?P<game_id>\d+)/$', stats.views.game_stats, name='show_game_stats'),
)